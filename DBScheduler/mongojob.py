'''
从Oracle数据库中（普光）读取测井曲线
'''
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
import lasio
import cx_Oracle  # 引用模块cx_Oracle
import time
import codecs
import os, sys, shutil
import pymysql
import pymongo
import logging
import inspect
import uuid

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#                    文件名，曲线名，间隔，测井曲线,开始深度，    结束深度
colNameList = ['JH', 'QXWJM', 'ZBMC', 'CYJG', 'ZBSJT', 'YXJDDJSD1', 'YXJDDJSD2']
#           mysql的连接地址
mysqlurl = 'mysql+pymysql://root:W3b5Ev!c3@127.0.0.1/petrol_data'


def getColIndex(colName):
    return colNameList.index(colName)


# 数据库列进入sql格式转换
def getCols():
    txt = ''
    for i in range(len(colNameList) - 1):
        txt += colNameList[i] + ','
    txt += colNameList[len(colNameList) - 1]
    return txt


def toDB(jh, tDepth, logNameList, logDataList):
    las = lasio.LASFile()
    samples = int(((tDepth[1] - tDepth[0]) / tDepth[2]) + 1)
    depth = np.linspace(tDepth[0], tDepth[1], samples)
    las.add_curve('DEPTH', depth, unit='M')
    for i in range(len(logNameList)):
        # print("==" * 20)
        # print("logNameList[i]", logNameList[i])
        # print("logDataList[i]", logDataList[i])
        las.add_curve(logNameList[i], logDataList[i], unit='UNKNOWN')
    las.well.WELL.value = jh
    df = las.df()
    print(df.head(10))


class Dbjob:
    def __init__(self, url, jh, qxwjm, linkstr, tablename):
        self.url = url
        self.jh = jh
        self.qxwjm = qxwjm
        # self.qx = qx
        self.linkstr = linkstr
        self.tablename = tablename

    # 井号进入sql格式转换
    def getjh(self):
        jh = self.jh
        jhvalues = jh.split(',')
        txt = ''
        for i in range(len(jhvalues) - 1):
            txt += jhvalues[i] + "','"
        txt += jhvalues[len(jhvalues) - 1]
        txt = "('" + txt + "')"
        return txt

    # 测井曲线进入sql格式转换
    def getqx(self):
        qx = self.qx
        txt = ''
        qxvalues = qx.split(',')
        for i in range(len(qxvalues) - 1):
            txt += qxvalues[i] + "','"
        txt += qxvalues[len(qxvalues) - 1]
        txt = "('" + txt + "')"
        return txt

    # 测井曲线文件名
    def getqxwjm(self):
        qxwjm = self.qxwjm
        qxwjmvals = qxwjm.split(',')

        txt = ''
        for i in range(len(qxwjmvals) - 1):
            txt += qxwjmvals[i] + "','"
        txt += qxwjmvals[len(qxwjmvals) - 1]
        txt = "('" + txt + "')"
        return txt

    def writeDB(self):
        sys_conn = cx_Oracle.connect(self.linkstr)
        cursor = sys_conn.cursor()  # 获取cursor
        sqlStr = 'SELECT %s from %s where JH in %s AND QXWJM in %s order by QXWJM' % (getCols(),
                                                                                      self.tablename, self.getjh(),
                                                                                      self.getqxwjm())

        cursor.execute(sqlStr.encode('utf-8'))

        result = cursor.fetchall()
        tDepth = [0.0, 0.0, 0.0]
        logNamelist = []
        logFieldlist = []
        logDatalist = []
        curJH = 'JH-Test-NONE'
        samples = 0
        lasCount = 0
        errorIndex = 0
        curLx = 'orignal filename'
        total_qx = len(result)
        for i in range(total_qx):
            jh = result[i][getColIndex('JH')]
            lx = result[i][getColIndex('QXWJM')].replace('.', '_')  # 测井曲线原来所属的文件名
            logName = result[i][getColIndex('ZBMC')]
            d1 = float(result[i][getColIndex('YXJDDJSD1')])
            d2 = float(result[i][getColIndex('YXJDDJSD2')])
            dd = float(result[i][getColIndex('CYJG')])
            if i == 0:
                curJH = jh
                curLx = lx
            if i == (total_qx - 1) or jh != curJH or lx != curLx or (
                    tDepth[0] != d1 or tDepth[1] != d2):
                if len(logNamelist) > 0:
                    toDB(curJH, tDepth, logNamelist, logDatalist)
                    lasCount += 1
                    logNamelist.clear()
                    logDatalist.clear()
                curJH = jh
                curLx = lx

                tDepth[0] = d1
                tDepth[1] = d2
                tDepth[2] = dd
                samples = int(((tDepth[1] - tDepth[0]) / tDepth[2]) + 1)
            tLog = result[i][getColIndex('ZBSJT')].read().decode('utf-8').split(' ')
            tData = np.ones(samples, dtype='float32')
            for j in range(0, min(samples, len(tLog))):
                try:
                    tData[j] = float(tLog[j].replace(' ', ''))
                except Exception as ex:
                    tData[j] = -999.25
                    tmpErr = '[errorIndex = %s]  i = %s, well = %s, tLog[j] = %s(j=%s, samples=%s), tLog[last] = %s ' % (
                        errorIndex, i, curJH, tLog[j], j, samples, tLog[len(tLog) - 1])
                    print('# # # ', tmpErr)

            logNamelist.append(logName)
            logFieldlist.append(logName)
            logDatalist.append(tData)

        toDB(jh, tDepth, logNamelist, logDatalist)
        sys_conn.close()


def function_logger(file_level, console_level=None):
    function_name = inspect.stack()[1][3]
    logger = logging.getLogger(function_name)
    logger.setLevel(logging.DEBUG)  # By default, logs all messages

    if console_level != None:
        ch = logging.StreamHandler()  # StreamHandler logs to console
        ch.setLevel(console_level)
        ch_format = logging.Formatter('%(asctime)s - %(message)s')
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    fh = logging.FileHandler("{0}.log".format(function_name))
    fh.setLevel(file_level)
    fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
    fh.setFormatter(fh_format)
    logger.addHandler(fh)

    return logger


if __name__ == '__main__':
    pass
