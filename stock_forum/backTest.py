# 并行遍历参数，查看每个参数的结果
import pandas as pd
from datetime import timedelta
from multiprocessing.pool import Pool
from datetime import datetime
import numpy as np
import itertools
from getStockData import Data_Reader

# =====计算资金曲线
# 交割合约资金曲线
def equity_curve_for_future_next_open(df, slippage=1 / 1000, c_rate=5 / 10000, leverage_rate=3, face_value=0.01,
                                                min_margin_ratio=1/100):
    """
    交割合约资金曲线
    开仓价格是下根K线的开盘价，可以是其他的形式
    相比之前杠杆交易的资金曲线函数，逻辑简单很多：手续费的处理、爆仓的处理等。
    在策略中增加滑点的。滑点的处理和手续费是不同的。
    :param df:
    :param slippage:  滑点 ，可以用百分比，也可以用固定值。
    :param c_rate:  手续费，commission fees，默认为万分之5。不同市场手续费的收取方法不同，对结果有影响。
    :param leverage_rate:  杠杆倍数
    :param face_value:  一张合约的面值
    :param min_margin_ratio: 最低保证金率，低于就会爆仓
    :return:
    """
    # =====下根k线开盘价
    df['next_open'] = df['open'].shift(-1)  # 下根K线的开盘价
    df['next_open'].fillna(value=df['close'], inplace=True)

    # =====找出开仓、平仓的k线
    condition1 = df['pos'] != 0  # 当前周期不为空仓
    condition2 = df['pos'] != df['pos'].shift(1)  # 当前周期和上个周期持仓方向不一样。
    open_pos_condition = condition1 & condition2

    condition1 = df['pos'] != 0  # 当前周期不为空仓
    condition2 = df['pos'] != df['pos'].shift(-1)  # 当前周期和下个周期持仓方向不一样。
    close_pos_condition = condition1 & condition2

    # =====对每次交易进行分组
    df.loc[open_pos_condition, 'start_time'] = df['candle_begin_time']
    df['start_time'].fillna(method='ffill', inplace=True)
    df.loc[df['pos'] == 0, 'start_time'] = pd.NaT

    # =====开始计算资金曲线
    initial_cash = 500000  # 初始资金，默认为500000元
    # ===在开仓时
    # 在open_pos_condition的K线，以开盘价计算买入合约的数量。（当资金量大的时候，可以用5分钟均价）
    df.loc[open_pos_condition, 'contract_num'] = initial_cash * leverage_rate / (face_value * df['open'])
    df['contract_num'] = np.floor(df['contract_num'])  # 对合约张数向下取整
    # 开仓价格：理论开盘价加上相应滑点
    df.loc[open_pos_condition, 'open_pos_price'] = df['open'] * (1 + slippage * df['pos'])
    # 开仓之后剩余的钱，扣除手续费
    df['cash'] = initial_cash - df['open_pos_price'] * face_value * df['contract_num'] * c_rate  # 即保证金

    # ===开仓之后每根K线结束时
    # 买入之后cash，contract_num，open_pos_price不再发生变动
    for _ in ['contract_num', 'open_pos_price', 'cash']:
        df[_].fillna(method='ffill', inplace=True)
    df.loc[df['pos'] == 0, ['contract_num', 'open_pos_price', 'cash']] = None

    # ===在平仓时
    # 平仓价格
    df.loc[close_pos_condition, 'close_pos_price'] = df['next_open'] * (1 - slippage * df['pos'])
    # 平仓之后剩余的钱，扣除手续费
    df.loc[close_pos_condition, 'close_pos_fee'] = df['close_pos_price'] * face_value * df['contract_num'] * c_rate

    # ===计算利润
    # 开仓至今持仓盈亏
    df['profit'] = face_value * df['contract_num'] * (df['close'] - df['open_pos_price']) * df['pos']
    # 平仓时理论额外处理
    df.loc[close_pos_condition, 'profit'] = face_value * df['contract_num'] * (
            df['close_pos_price'] - df['open_pos_price']) * df['pos']
    # 账户净值
    df['net_value'] = df['cash'] + df['profit']

    # ===计算爆仓
    # 至今持仓盈亏最小值
    df.loc[df['pos'] == 1, 'price_min'] = df['low']
    df.loc[df['pos'] == -1, 'price_min'] = df['high']
    df['profit_min'] = face_value * df['contract_num'] * (df['price_min'] - df['open_pos_price']) * df['pos']
    # 账户净值最小值
    df['net_value_min'] = df['cash'] + df['profit_min']
    # 计算保证金率
    df['margin_ratio'] = df['net_value_min'] / (face_value * df['contract_num'] * df['price_min'])
    # 计算是否爆仓
    df.loc[df['margin_ratio'] <= (min_margin_ratio + c_rate), '是否爆仓'] = 1

    # ===平仓时扣除手续费
    df.loc[close_pos_condition, 'net_value'] -= df['close_pos_fee']
    # 应对偶然情况：下一根K线开盘价格价格突变，在平仓的时候爆仓。此处处理有省略，不够精确。
    df.loc[close_pos_condition & (df['net_value'] < 0), '是否爆仓'] = 1

    # ===对爆仓进行处理
    df['是否爆仓'] = df.groupby('start_time')['是否爆仓'].fillna(method='ffill')
    df.loc[df['是否爆仓'] == 1, 'net_value'] = 0

    # =====计算资金曲线
    df['equity_change'] = df['net_value'].pct_change()
    df.loc[open_pos_condition, 'equity_change'] = df.loc[open_pos_condition, 'net_value'] / initial_cash - 1  # 开仓日的收益率
    df['equity_change'].fillna(value=0, inplace=True)
    df['equity_curve'] = (1 + df['equity_change']).cumprod()

    # =====删除不必要的数据，并存储
    df.drop(['next_open', 'contract_num', 'open_pos_price', 'cash', 'close_pos_price', 'close_pos_fee',
             'profit', 'net_value', 'price_min', 'profit_min', 'net_value_min', 'margin_ratio', '是否爆仓'],
            axis=1, inplace=True)

    return df

# 由交易信号产生实际持仓
def position_for_future(df):
    """
    根据signal产生实际持仓。考虑各种不能买入卖出的情况。
    所有的交易都是发生在产生信号的K线的结束时
    :param df:
    :return:
    """

    # ===由signal计算出实际的每天持有仓位
    # 在产生signal的k线结束的时候，进行买入
    df['signal'].fillna(method='ffill', inplace=True)
    df['signal'].fillna(value=0, inplace=True)  # 将初始行数的signal补全为0
    df['pos'] = df['signal'].shift()
    df['pos'].fillna(value=0, inplace=True)  # 将初始行数的pos补全为0

    # ===对无法买卖的时候做出相关处理
    # 例如：下午4点清算，无法交易；股票、期货当天涨跌停的时候无法买入；股票的t+1交易制度等等。
    # 当前周期持仓无法变动的K线
    condition = (df['candle_begin_time'].dt.hour == 16) & (df['candle_begin_time'].dt.minute == 0)
    df.loc[condition, 'pos'] = None
    # pos为空的时，不能买卖，只能和前一周期保持一致。
    df['pos'].fillna(method='ffill', inplace=True)

    # 在实际操作中，不一定会直接跳过4点这个周期，而是会停止N分钟下单。此时可以注释掉上面的代码。

    # ===将数据存入hdf文件中
    # 删除无关中间变量
    df.drop(['signal'], axis=1, inplace=True)

    return df

# =====简单布林策略
# 策略
def signal_simple_bolling(df, para=[200, 2]):
    """
    :param df:
    :param para: n, m
    :return:

    # 布林线策略
    # 布林线中轨：n天收盘价的移动平均线
    # 布林线上轨：n天收盘价的移动平均线 + m * n天收盘价的标准差
    # 布林线上轨：n天收盘价的移动平均线 - m * n天收盘价的标准差
    # 当收盘价由下向上穿过上轨的时候，做多；然后由上向下穿过中轨的时候，平仓。
    # 当收盘价由上向下穿过下轨的时候，做空；然后由下向上穿过中轨的时候，平仓。
    """

    # ===策略参数
    n = int(para[0])
    m = para[1]

    # ===计算指标
    # 计算均线
    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    # 计算上轨、下轨道
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)  # ddof代表标准差自由度
    df['upper'] = df['median'] + m * df['std']
    df['lower'] = df['median'] - m * df['std']

    # ===计算信号
    # 改进信号
    condition3 = abs((df['close']-df['median'])/df['median']) < 0.05 # 收盘价不能偏离均线太远

    # 找出做多信号
    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    df.loc[condition1 & condition2 & condition3, 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # 找出做多平仓信号
    condition1 = df['close'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['close'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    df.loc[condition1 & condition2, 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 找出做空信号
    condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    df.loc[condition1 & condition2 & condition3, 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

    # 找出做空平仓信号
    condition1 = df['close'] > df['median']  # 当前K线的收盘价 > 中轨
    condition2 = df['close'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    df.loc[condition1 & condition2, 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # 合并做多做空信号，去除重复信号
    df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1, skipna=True)  # 若你的pandas版本是最新的，请使用本行代码代替上面一行
    temp = df[df['signal'].notnull()][['signal']]
    temp = temp[temp['signal'] != temp['signal'].shift(1)]
    df['signal'] = temp['signal']

    # ===删除无关变量
    df.drop(['median', 'std', 'upper', 'lower', 'signal_long', 'signal_short'], axis=1, inplace=True)

    return df


# 策略参数组合
def signal_simple_bolling_para_list(m_list=range(10, 500, 10), n_list=[i / 10 for i in list(np.arange(5, 50, 1))]):
    """
    产生布林 策略的参数范围
    :param m_list:
    :param n_list:
    :return:
    """
    para_list = []

    for m in m_list:
        for n in n_list:
            para = [m, n]
            para_list.append(para)

    return para_list

# =====参数设定
# 手工设定策略参数
symbol = '中证500'

face_value = 0.2  # 合约面值
c_rate = 0.5 / 10000  # 手续费，取万分之0.5
slippage = 1 / 1000  # 滑点 ，可以用百分比，取0.1%
leverage_rate = 1 # 杠杆倍数
min_margin_ratio = 1 / 10  # 最低保证金率，低于就会爆仓，取10%
drop_days = 100  # 刚刚上线100天内不交易


# =====读入数据
dr=Data_Reader()
df = dr.getStockIndex(symbol)
df.rename(columns={
    '时间':'candle_begin_time',
    '开盘':'open',
    '最高':'high',
    '最低':'low',
    '收盘':'close',
    '成交量':'volume',
    '成交额':'volume_value',
}, inplace=True)
df['candle_begin_time']=df['candle_begin_time'].astype('str')
df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])
df.sort_values(by=['candle_begin_time'], inplace=True)
df.drop_duplicates(subset=['candle_begin_time'], inplace=True)
df = df[df['volume'] > 0]  # 去除成交量为0的交易周期
df.reset_index(inplace=True, drop=True)


# =====获取策略参数组合
# para_list = signal_simple_bolling_para_list(m_list=range(15, 25, 1), n_list=[i / 100 for i in list(np.arange(50, 150, 1))])
para_list = [[18, 0.67]]

# =====单次循环
def calculate_by_one_loop(para):
    _df = df.copy()
    # 计算交易信号
    _df = signal_simple_bolling(_df, para=para)
    # 计算实际持仓
    _df = position_for_future(_df)
    # 计算资金曲线
    # 选取相关时间。上线10天之后的日期
    t = pd.to_datetime(_df.iloc[0]['candle_begin_time']) + timedelta(days=drop_days)
    _df = _df[_df['candle_begin_time'] > t]
    # 计算资金曲线
    _df = equity_curve_for_future_next_open(_df, slippage=slippage, c_rate=c_rate, leverage_rate=leverage_rate,
                                                      face_value=face_value, min_margin_ratio=min_margin_ratio)
    # 保存资金曲线
    _df.to_csv('analysis/%s_equity_curve.csv'%symbol, encoding='gbk') 
    # 计算收益
    rtn = pd.DataFrame()
    rtn.loc[0, 'para'] = str(para)
    r = _df.iloc[-1]['equity_curve']
    rtn.loc[0, 'equity_curve'] = r
    print(para, '策略最终收益：', r)
    return rtn


if __name__ == "__main__":
    # =====并行提速
    start_time = datetime.now()  # 标记开始时间
    with Pool(processes=4) as pool:  # or whatever your hardware can support
        # 使用并行批量获得data frame的一个列表
        df_list = pool.map(calculate_by_one_loop, para_list)
        print('读入完成, 开始合并', datetime.now() - start_time)
        # 合并为一个大的DataFrame
        para_curve_df = pd.concat(df_list, ignore_index=True)

    # =====输出
    para_curve_df.sort_values(by='equity_curve', ascending=False, inplace=True)
    print(para_curve_df)
    para_curve_df.to_csv('back_test_result/%s_back_test_result.csv' % symbol)
