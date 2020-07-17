import requests
import random
import pandas as pd

class Data_Reader(object):
    # 初始化数据
    def __init__(self):
        self.server = 'http://yunhq.sse.com.cn' # 数据接口
        self.market_type='sh1' # 市场类型 sz1为深证A股,sh1为上证A股
        self.code='000001' # 股票代码
        self.line_type='line' # line为分时线, dayk为k线
        self.begin='0'
        self.end='-1' # 获取数据的起始,(0,-1)表示所有,(i,j)表示数据库的第i到第j条数据
        self.data_url=''
        
    # 设置参数
    def setCondition(self):
        self.data_url=self.server+':32041/v1/'+self.market_type+'/'+self.line_type+'/'+self.code+'?begin='+self.begin+'&end='+self.end
        # print(self.data_url)

    # 获取股票行情数据 code为股票代码,line_type为图线数据类型(line为分时线, dayk为k线)
    # 返回dataframe数据
    def getStockQuotesData(self,code,line_type,back_range):
        if back_range == -1: # 输入-1则获取全部数据
            self.begin='0'
        else: # 获取back_range条数据
            self.begin=str(-back_range-1)
        if code[0]=='6':
            self.market_type='sh1'
        elif code[0:2]=='sh':
            self.market_type='sh1'
            code = code[2:]
        elif code[0]=='0':
            self.market_type='sz1'
        elif code[0:2]=='sz':
            self.market_type='sz1'
            code = code[2:]

        if line_type=='分时':
            self.line_type='line'
        elif line_type=='k线':
            self.line_type='dayk'
        else:
            print('参数错误')
        self.code=code
        self.setCondition()
        req = requests.get(url=self.data_url)
        origin_data = req.json()
        if line_type=='分时':
            col=['最新','均价','成交量']
            origin_data=origin_data['line']
        elif line_type=='k线':
            col=['时间','开盘','最高','最低','收盘','成交量','成交额']
            origin_data=origin_data['kline']
        else:
            print('参数错误')
        df=pd.DataFrame(origin_data,columns=col)
        return df
    
    # 获取深证A股股票数据
    # 返回dataframe数据
    def getSzStockList(self):
        req = requests.get(url='http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1110x&TABKEY=tab1&random='+str(random.random()))
        stock_list=pd.read_excel(req.content,converters = {'A股代码':str})
        return stock_list
    
    # 获取上证A股股票数据
    # 返回dataframe数据
    def getShStockList(self):
        req = requests.get(url='http://query.sse.com.cn/security/stock/downloadStockListFile.do?stockType=1',headers={
            'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
        })
        res=req.content.decode('gbk').split('\n')
        for i in (range(len(res))):
            res[i]=res[i].split('\t')[0:5]
        for i in range(len(res)):
            for j in range(len(res[i])):
                res[i][j]=res[i][j].replace(' ','')
        df=pd.DataFrame(res[1:-1],columns=res[0])
        return df
    
    # 获取股票指数数据
    # 返回dataframe数据
    def getStockIndex(self, name):
        if name == '中证500' or name == 'ZhongZheng500': 
            res = self.getStockQuotesData('sh000905', 'k线', -1)
        elif name == '上证50' or name == 'ShangZheng50':
            res = self.getStockQuotesData('sh000016', 'k线', -1)
        elif name == '上证指数' or name == 'ShangZhengZhiShu':
            res = self.getStockQuotesData('sh000001', 'k线', -1)
        elif name == '沪深300' or name == 'HuShen300':
            res = self.getStockQuotesData('sh000300', 'k线', -1)
        elif name == '深证成指' or name == 'ShenZhengChengZhi':
            res = self.getStockQuotesData('sz399001', 'k线', -1)
        return res

if __name__ == "__main__":
    dr=Data_Reader()
    # print(dr.getShStockList())
    # print(dr.strategy('galileo'))
    # print(dr.getClassification())
    print(dr.getStockQuotesData('600001','k线',-1))