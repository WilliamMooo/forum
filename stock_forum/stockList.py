import pymysql
import pandas as pd

import config
from getStockData import Data_Reader

# 连接数据库
def conn():
    db = pymysql.connect(host=config.host, port=config.port, user=config.user, passwd=config.password, db=config.db, charset=config.charset)
    return db

# 使用cursor()方法获取操作游标 
def getCursor(db):
    cursor = db.cursor()
    return cursor

# 打印数据库版本
def dbVertion(cursor):
    cursor.execute("select version()")
    Version = cursor.fetchone()
    print(" Database Version:%s" % Version)

# 创建股票列表
def createStockList(cursor):
    # 创建数据表SQL语句
    sql = """CREATE TABLE `stock_list` (
            `code` CHAR(6) NOT NULL,
            `name` CHAR(20),
            `listing_date` DATE,
            PRIMARY KEY(`code`))"""
    cursor.execute(sql)

# 删除股票列表
def delStockList(cursor):
    # 如果数据表STOCK_LIST已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS `stock_list`")

# 删除股票列表中的数据
def delListEle(cursor):
    sql = "DELETE FROM `stock_list`"
    # 执行sql语句
    cursor.execute(sql)

# 向数据库插入数据
def insertEle(cursor, code, name, date):
    sql = 'INSERT INTO `stock_list`(`code`, `name`, `listing_date`) VALUES ("' + code + '","' + name + '","' + date + '")'
    try:
        cursor.execute(sql)
    except:
        db.rollback()

# 关闭数据库
def closeDB(db):
    db.close()


if __name__ == "__main__":
    db=conn() # 连接数据库
    cursor=getCursor(db)
    dbVertion(cursor) # 测试连接是否成功
    delStockList(cursor) # 删除股票列表
    createStockList(cursor) # 创建股票列表
    delListEle(cursor) # 删除股票列表中的数据

    # # 从爬虫读取A股数据
    rd=Data_Reader()
    data0=rd.getShStockList()
    data1=rd.getSzStockList().applymap(str)
    # 向数据库插入数据
    for i in range(len(data0)):
        insertEle(cursor, data0['代码'][i], data0['简称'][i], data0['上市日期'][i])
    for i in range(len(data1)):
        insertEle(cursor, data1['A股代码'][i], data1['A股简称'][i], data1['A股上市日期'][i])
    closeDB(db)

    # 提交到数据库执行
    db.commit()
    # 统计表的数量sql: SELECT count(TABLE_NAME) FROM information_schema.TABLES WHERE TABLE_SCHEMA='dbname'; 