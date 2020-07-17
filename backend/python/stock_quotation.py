import pandas as pd
import pymysql
from time import sleep

import config
from get_stock_data import Data_Reader

# 获取股票列表
def getStockList():
    db = pymysql.connect(host=config.host, port=config.port, user=config.user, passwd=config.password, db=config.db, charset=config.charset)
    cursor = db.cursor()
    sql = 'SELECT `code` from `stock_list`'
    cursor.execute(sql)
    results = cursor.fetchall()
    codes = []
    for i in range(len(results)):
        codes.append(results[i][0])
    db.close()
    return codes


# 插入到空数据库
def insertToEmptyDb():
    insertIndexData()
    codes=getStockList()
    db = pymysql.connect(host=config.host, port=config.port, user=config.user, passwd=config.password, db=config.db, charset=config.charset)
    cursor = db.cursor()
    dr = Data_Reader()
    for code in codes:
        data = dr.getStockQuotesData(code,'k线',-1).applymap(str)
        sql_create = 'CREATE TABLE `' + code + """`  (
            `time` DATE NOT NULL,
            PRIMARY KEY (`time`),
            `open` FLOAT,
            `close` FLOAT,
            `low` FLOAT,
            `high` FLOAT,
            `volume` BIGINT,
            `amount` BIGINT ) ENGINE = InnoDB DEFAULT CHARSET = utf8; \n """
        sql_insert = 'INSERT INTO `'+code+"""` (
            `time`, `open`, `close`, `low`, `high`, `volume`, `amount`)
            VALUES """
        for j in range(len(data)):
            sql_insert += '("' + data['时间'][j] + '",' + data['开盘'][j] + ',' + data['收盘'][j] + ',' + data['最低'][j]\
                + ',' + data['最高'][j] + ',' + data['成交量'][j]\
                + ',' + data['成交额'][j] + '),'
        try:
            # 执行sql语句
            cursor.execute(sql_create)
            cursor.execute(sql_insert[:-1])
            # 提交到数据库
            db.commit()
        except:
            db.rollback()
    # 关闭数据库
    db.close()

# 插入指数数据
def insertIndexData():
    db = pymysql.connect(host=config.host, port=config.port, user=config.user, passwd=config.password, db=config.db, charset=config.charset)
    cursor = db.cursor()
    dr = Data_Reader()
    symbol_list = ['ZhongZheng500', 'ShangZheng50', 'ShangZhengZhiShu', 'HuShen300', 'ShenZhengChengZhi']
    for symbol in symbol_list:
        data = dr.getStockIndex(symbol).applymap(str)
        sql_create = 'CREATE TABLE `' + symbol + """`  (
            `time` DATE NOT NULL,
            PRIMARY KEY (`time`),
            `open` FLOAT,
            `close` FLOAT,  
            `low` FLOAT,
            `high` FLOAT,
            `volume` BIGINT,
            `amount` BIGINT ) ENGINE = InnoDB DEFAULT CHARSET = utf8; \n """
        sql_insert = 'INSERT INTO `'+symbol+"""` (
            `time`, `open`, `close`, `low`, `high`, `volume`, `amount`)
            VALUES """
        for j in range(len(data)):
            sql_insert += '("' + data['时间'][j] + '",' + data['开盘'][j] + ',' + data['收盘'][j] + ',' + data['最低'][j]\
                + ',' + data['最高'][j] + ',' + data['成交量'][j]\
                + ',' + data['成交额'][j] + '),'
        try:
            # 执行sql语句
            cursor.execute(sql_create)
            cursor.execute(sql_insert[:-1])
            # 提交到数据库
            db.commit()
        except:
            db.rollback()
    # 关闭数据库
    db.close()

# 插入更新数据库 num为今天往前推的天数
def insertAndUpdate(num):
    dr = Data_Reader()
    db = pymysql.connect(host=config.host, port=config.port, user=config.user, passwd=config.password, db=config.db, charset=config.charset)
    cursor = db.cursor()
    # 更新指数数据
    symbol_list = ['ZhongZheng500', 'ShangZheng50', 'ShangZhengZhiShu', 'HuShen300', 'ShenZhengChengZhi']
    for symbol in symbol_list:
        data = dr.getStockIndex(symbol).applymap(str)
        # 查询数据库中是否存在该指数
        sql = "SHOW TABLES LIKE '"+symbol+"'"
        if cursor.execute(sql)>0: # 存在则进行插入和更新
            print(symbol+'存在')
        else: # 不存在则创建
            print(symbol+'不存在')
            # 创建数据表SQL语句
            sql = 'CREATE TABLE `' + symbol + """`  (
                    `time` DATE NOT NULL,
                    PRIMARY KEY (`time`),
                    `open` FLOAT,
                    `close` FLOAT,  
                    `low` FLOAT,
                    `high` FLOAT,
                    `volume` BIGINT,
                    `amount` BIGINT )"""
            cursor.execute(sql)
        # 插入和更新数据
        for j in range(len(data)):
            sql = "SELECT `time` FROM `" + symbol + "` WHERE `time`='" + data['时间'][j] + "'"
            if cursor.execute(sql)>0:
                # 向数据库更新数据
                # print("更新"+data['时间'][j])
                sql = "UPDATE `"+symbol+"` SET `open` = '"+data['开盘'][j]+"', `close` = '"+data['收盘'][j]+"', `low` = '"+data['最低'][j]\
                    +"', `high` = '"+data['最高'][j]+"', `volume` = '"+\
                    data['成交量'][j]+" ', `amount` = '"+data['成交额'][j]+" ' WHERE `"+symbol+"`.`time` = '"+data['时间'][j]+"'"
            else:
                # 向数据库插入数据
                # print("插入"+data['时间'][j])
                sql = 'INSERT INTO `'+symbol+"""` (
                    `time`, `open`, `close`, `low`, `high`, `volume`, `amount`)
                    VALUES ("""
                sql += '"' + data['时间'][j] + '",' + data['开盘'][j] + ',' + data['收盘'][j] + ',' + data['最低'][j]\
                    + ',' + data['最高'][j] + ',' + data['成交量'][j]\
                    + ',' + data['成交额'][j] + ')'
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                db.rollback()
    # 更新股票数据
    codes=getStockList()
    for code in codes:
        # 爬取股票数据
        data = dr.getStockQuotesData(code,'k线',num).applymap(str)
        # 查询数据库中是否存在该股票
        sql = "SHOW TABLES LIKE '"+code+"'"
        if cursor.execute(sql)>0: # 存在则进行插入和更新
            print(code+'存在')
        else: # 不存在则创建
            print(code+'不存在')
            # 创建数据表SQL语句
            sql = 'CREATE TABLE `' + code + """`  (
                    `time` DATE NOT NULL,
                    PRIMARY KEY (`time`),
                    `open` FLOAT,
                    `close` FLOAT,  
                    `low` FLOAT,
                    `high` FLOAT,
                    `volume` BIGINT,
                    `amount` BIGINT )"""
            cursor.execute(sql)
        # 插入和更新数据
        for j in range(len(data)):
            sql = "SELECT `time` FROM `" + code + "` WHERE `time`='" + data['时间'][j] + "'"
            if cursor.execute(sql)>0:
                # 向数据库更新数据
                # print("更新"+data['时间'][j])
                sql = "UPDATE `"+code+"` SET `open` = '"+data['开盘'][j]+"', `close` = '"+data['收盘'][j]+"', `low` = '"+data['最低'][j]\
                    +"', `high` = '"+data['最高'][j]+"', `volume` = '"+\
                    data['成交量'][j]+" ', `amount` = '"+data['成交额'][j]+" ' WHERE `"+code+"`.`time` = '"+data['时间'][j]+"'"
            else:
                # 向数据库插入数据
                # print("插入"+data['时间'][j])
                sql = 'INSERT INTO `'+code+"""` (
                    `time`, `open`, `close`, `low`, `high`, `volume`, `amount`)
                    VALUES ("""
                sql += '"' + data['时间'][j] + '",' + data['开盘'][j] + ',' + data['收盘'][j] + ',' + data['最低'][j]\
                    + ',' + data['最高'][j] + ',' + data['成交量'][j]\
                    + ',' + data['成交额'][j] + ')'
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                db.rollback()
    # 关闭数据库
    db.close()

if __name__ == "__main__":
    # insertToEmptyDb()
    # insertIndexData()
    while True:
        insertAndUpdate(1)
        sleep(86400)