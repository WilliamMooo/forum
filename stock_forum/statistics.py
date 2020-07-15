# 策略评价函数
import pandas as pd
import numpy as np
import itertools
import pymysql
import config

# ======= 策略评价 =========
# 将资金曲线数据，转化为交易数据
def transfer_equity_curve_to_trade(equity_curve):
    """
    将资金曲线数据，转化为一笔一笔的交易
    :param equity_curve: 资金曲线函数计算好的结果，必须包含pos
    :return:
    """
    # =选取开仓、平仓条件
    condition1 = equity_curve['pos'] != 0
    condition2 = equity_curve['pos'] != equity_curve['pos'].shift(1)
    open_pos_condition = condition1 & condition2

    # =计算每笔交易的start_time
    if 'start_time' not in equity_curve.columns:
        equity_curve.loc[open_pos_condition, 'start_time'] = equity_curve['candle_begin_time']
        equity_curve['start_time'].fillna(method='ffill', inplace=True)
        equity_curve.loc[equity_curve['pos'] == 0, 'start_time'] = pd.NaT

    # =对每次交易进行分组，遍历每笔交易
    trade = pd.DataFrame()  # 计算结果放在trade变量中

    for _index, group in equity_curve.groupby('start_time'):

        # 记录每笔交易
        # 本次交易方向
        trade.loc[_index, 'signal'] = group['pos'].iloc[0]

        # 本次交易杠杆倍数
        if 'leverage_rate' in group:
            trade.loc[_index, 'leverage_rate'] = group['leverage_rate'].iloc[0]

        g = group[group['pos'] != 0]  # 去除pos=0的行
        # 本次交易开始那根K线的开始时间
        trade.loc[_index, 'start_bar'] = g.iloc[0]['candle_begin_time']
        # 本次交易结束那根K线的开始时间
        trade.loc[_index, 'end_bar'] = g.iloc[-1]['candle_begin_time']
        # 开仓价格
        trade.loc[_index, 'start_price'] = g.iloc[0]['open']
        # 平仓信号的价格
        trade.loc[_index, 'end_price'] = g.iloc[-1]['close']
        # 持仓k线数量
        trade.loc[_index, 'bar_num'] = g.shape[0]
        # 本次交易收益
        trade.loc[_index, 'change'] = (group['equity_change'] + 1).prod() - 1
        # 本次交易结束时资金曲线
        trade.loc[_index, 'end_equity_curve'] = g.iloc[-1]['equity_curve']
        # 本次交易中资金曲线最低值
        trade.loc[_index, 'min_equity_curve'] = g['equity_curve'].min()

    return trade


# 计算策略评价指标
def strategy_evaluate(equity_curve, trade):
    """
    :param equity_curve: 带资金曲线的df
    :param trade: transfer_equity_curve_to_trade的输出结果，每笔交易的df
    :return:
    """
    # ===新建一个dataframe保存回测指标
    results = pd.DataFrame()

    # ===计算累积净值
    results.loc[0, '累积净值'] = round(equity_curve['equity_curve'].iloc[-1], 2)

    # ===计算年化收益
    annual_return = (equity_curve['equity_curve'].iloc[-1] / equity_curve['equity_curve'].iloc[0]) ** (
        '1 days 00:00:00' / (equity_curve['candle_begin_time'].iloc[-1] - equity_curve['candle_begin_time'].iloc[0]) * 365) - 1
    results.loc[0, '年化收益'] = str(round(annual_return, 4))

    # ===计算最大回撤
    # 计算当日之前的资金曲线的最高点
    equity_curve['max2here'] = equity_curve['equity_curve'].expanding().max()
    # 计算到历史最高值到当日的跌幅，drowdwon
    equity_curve['dd2here'] = equity_curve['equity_curve'] / equity_curve['max2here'] - 1
    # 计算最大回撤，以及最大回撤结束时间
    end_date, max_draw_down = tuple(equity_curve.sort_values(by=['dd2here']).iloc[0][['candle_begin_time', 'dd2here']])
    # 计算最大回撤开始时间
    start_date = equity_curve[equity_curve['candle_begin_time'] <= end_date].sort_values(by='equity_curve', ascending=False).iloc[0]['candle_begin_time']
    # 将无关的变量删除
    equity_curve.drop(['max2here', 'dd2here'], axis=1, inplace=True)
    results.loc[0, '最大回撤'] = format(max_draw_down, '.2%')
    results.loc[0, '最大回撤开始时间'] = str(start_date)
    results.loc[0, '最大回撤结束时间'] = str(end_date)

    # ===年化收益/回撤比
    results.loc[0, '年化收益/回撤比'] = round(abs(annual_return / max_draw_down), 2)

    # ===统计每笔交易
    results.loc[0, '盈利笔数'] = len(trade.loc[trade['change'] > 0])  # 盈利笔数
    results.loc[0, '亏损笔数'] = len(trade.loc[trade['change'] <= 0])  # 亏损笔数
    results.loc[0, '胜率'] = format(results.loc[0, '盈利笔数'] / len(trade))  # 胜率

    results.loc[0, '每笔交易平均盈亏'] = format(trade['change'].mean(), '.2%')  # 每笔交易平均盈亏
    results.loc[0, '盈亏收益比'] = round(trade.loc[trade['change'] > 0]['change'].mean() / \
                                    trade.loc[trade['change'] < 0]['change'].mean() * (-1), 2)  # 盈亏比

    results.loc[0, '单笔最大盈利'] = trade['change'].max()  # 单笔最大盈利
    results.loc[0, '单笔最大亏损'] = trade['change'].min()  # 单笔最大亏损

    # ===统计持仓时间，会比实际时间少一根K线的是距离
    trade['持仓时间'] = trade['end_bar'] - pd.to_datetime(trade.index)
    max_days = trade['持仓时间'].max().days
    results.loc[0, '单笔最长持有时间'] = str(max_days) + ' 天 '  # 单笔最长持有时间

    min_days = trade['持仓时间'].min().days
    results.loc[0, '单笔最短持有时间'] = str(min_days) + ' 天 '  # 单笔最短持有时间

    mean_days = trade['持仓时间'].mean().days
    results.loc[0, '平均持仓周期'] = str(mean_days) + ' 天 '  # 平均持仓周期

    # ===连续盈利亏算
    results.loc[0, '最大连续盈利笔数'] = max(
        [len(list(v)) for k, v in itertools.groupby(np.where(trade['change'] > 0, 1, np.nan))])  # 最大连续盈利笔数
    results.loc[0, '最大连续亏损笔数'] = max(
        [len(list(v)) for k, v in itertools.groupby(np.where(trade['change'] < 0, 1, np.nan))])  # 最大连续亏损笔数

    # ===每月收益率
    equity_curve.set_index('candle_begin_time', inplace=True)
    monthly_return = equity_curve[['equity_change']].resample(rule='M').apply(lambda x: (1 + x).prod() - 1)

    return results, monthly_return


if __name__ == "__main__":
    # 读取资金曲线数据
    method = '布林策略'
    symbol = '中证500'
    description = '中轨=前m天的收盘价均线，上轨=中轨+n*前m天的收盘价标准差，下轨=中轨-n*前m天的收盘价标准差。当收盘价由下向上穿过上轨的时候，做多；然后由上向下穿过中轨的时候，平仓。当收盘价由上向下穿过下轨的时候，做空；然后由下向上穿过中轨的时候，平仓。'
    equity_curve = pd.read_csv('analysis/%s_equity_curve.csv' % symbol)
    equity_curve['candle_begin_time'] = pd.to_datetime(equity_curve['candle_begin_time'])
    # print(equity_curve)

    # 计算每笔交易
    trade = transfer_equity_curve_to_trade(equity_curve)
    print(trade)

    # 计算各类统计指标
    r, monthly_return = strategy_evaluate(equity_curve, trade)

    print(r)
    # print(max(monthly_return['equity_change']), min(monthly_return['equity_change']))
    print('-'*30)
    # 将分析结果保存到数据库
    # 连接数据库
    db = pymysql.connect(host=config.host, port=config.port, user=config.user, passwd=config.password, db=config.db, charset=config.charset)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 查找数据库中是否存在该策略，存在则更新，不存在则创建
        sql = 'SELECT `id` from `strategy` where `name`= "' + method + '_' + symbol + '";'
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        if len(results) == 1: # 更新数据
            curve_id = results[0][0]
            # 删除数据表原数据
            sql = 'DELETE FROM `equity_curve_'+str(curve_id)+'`'
            cursor.execute(sql)
            # 插入新数据
            sql = 'insert into `equity_curve_'+str(curve_id)+'` (`start`, `end`, `equity`, `signal`, `change`) values '
            for i in range(len(trade)):
                sql +=  '("'+str(trade['start_bar'].values[i])[0:10] + '", "' + str(trade['end_bar'].values[i])[0:10] + '", ' + str(trade['end_equity_curve'].values[i]) +\
                    ', ' + str(trade['signal'].values[i]) + ', ' + str(trade['change'].values[i]) + '),'
            # print(sql)
            cursor.execute(sql[:-1])
        elif len(results) == 0: # 插入新数据
            # 插入数据表
            sql = 'insert into `strategy`(`name`, `description`, `equity_sum`, `annualised_return`, `win_count`, `max_win`, `lose_count`, `max_lose`, `average_hold`) values("'+\
                method + '_' + symbol + '", "' + description + '", ' + str(r['累积净值'].values[0]) + ', ' + str(r['年化收益'].values[0]) + ', ' + str(r['盈利笔数'].values[0]) +\
                ', ' + str(r['单笔最大盈利'].values[0]) + ', ' + str(r['亏损笔数'].values[0]) + ', ' + str(r['单笔最大亏损'].values[0]) + ', "' + str(r['平均持仓周期'].values[0]) +'")'
            cursor.execute(sql)
            db.commit()
            db.rollback()
            sql = 'SELECT `id` from `strategy` where `name`= "' + method + '_' + symbol + '";'
            cursor.execute(sql)
            results = cursor.fetchall()
            curve_id = results[0][0]
            # 创建数据表SQL语句
            sql = 'CREATE TABLE `equity_curve_' + str(curve_id) + '''` (
                    `start` DATE NOT NULL,
                    `end` DATE NOT NULL,
                    `equity` FLOAT NOT NULL,
                    `signal` INT NOT NULL,
                    `change` FLOAT NOT NULL,
                    PRIMARY KEY(`start`),
                    KEY(`end`)
                    )'''
            cursor.execute(sql)
            # 插入新数据
            sql = 'insert into `equity_curve_'+str(curve_id)+'` (`time`, `equity`) values '
            for i in range(len(trade)):
                sql +=  '("'+str(trade['end_bar'].values[i])[0:10] + '", ' + str(trade['end_equity_curve'].values[i]) + '),'
            cursor.execute(sql[:-1])
        else:
            print('策略出现重名')
        db.commit()
    except:
        db.rollback()
    finally:
        # 关闭数据库
        db.close()