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
# import pymysql
import pymongo
import logging
import inspect
import uuid

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#                    文件名，曲线名，间隔，测井曲线,开始深度，    结束深度
colNameList = ['JH', 'QXWJM', 'ZBMC', 'CYJG', 'ZBSJT', 'YXJDDJSD1', 'YXJDDJSD2']
#           mysql的连接地址
mysqlurl = 'mysql+pymysql://root:W3b5Ev!c3@127.0.0.1/petrol_data'


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


def getColIndex(colName):
    return colNameList.index(colName)


# 数据库列进入sql格式转换
def getCols():
    txt = ''
    for i in range(len(colNameList) - 1):
        txt += colNameList[i] + ','
    txt += colNameList[len(colNameList) - 1]
    return txt


'''
options, args = getopt.getopt(sys.argv[1 :], 'u:j:x:q:')
for name, value in options :
    if name in ('-u') :
        url = value
    if name in ('-j') :
        jh = value.split(",")
    if name in ('-x') :
        qxwjm = value.split(",")
    if name in ('-q') :
        qx = value.split(",")
'''


class Dbjob:
    def __init__(self, url, jh, qxwjm, outPath):
        self.url = url
        self.jh = jh
        self.qxwjm = qxwjm
        # self.qx = qx
        self.outPath = outPath

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

    def writeLog(self):
        fwrite_logger = function_logger(logging.DEBUG, logging.ERROR)
        linkstr = self.url
        outPath = self.outPath
        fWrite = codecs.open(outPath + '/writeLog.log', 'w', encoding='gbk')
        # strOrder = '%s/%s@%s:%s/%s' % (userName, passWord, ip, str(port), sid)

        sys_conn = cx_Oracle.connect(linkstr)
        # sys_conn=cx_Oracle.connect('truck/******@10.74.**.**:****/****')    #连接数据库
        cursor = sys_conn.cursor()  # 获取cursor
        # sqlStr = 'SELECT %s from WL18 order by QXWJM'%(getCols())
        # print(self.getjh())
        sqlStr = 'SELECT %s from WL18 where JH in %s AND QXWJM in %s order by QXWJM' % (
        getCols(), self.getjh(), self.getqxwjm())

        fwrite_logger.debug(sqlStr)
        cursor.execute(sqlStr.encode('utf-8'))
        # cursor.execute(sqlStr)
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
        # print('result', len(result))
        fwrite_logger.debug(len(result))
        total_qx = len(result)
        for i in range(total_qx):
            # print('i', i, result[i])
            jh = result[i][getColIndex('JH')]
            lx = result[i][getColIndex('QXWJM')].replace('.', '_')  # 测井曲线原来所属的文件名
            logName = result[i][getColIndex('ZBMC')]
            d1 = float(result[i][getColIndex('YXJDDJSD1')])
            d2 = float(result[i][getColIndex('YXJDDJSD2')])
            dd = float(result[i][getColIndex('CYJG')])
            if i == 0:
                curJH = jh
                curLx = lx
                curPath = outPath + '/' + curJH
                if os.path.exists(curPath) == False:  # 每一个井建立一个子文件夹
                    os.mkdir(curPath)

            # print('check param:','jh',jh,'curJH',curJH,'lx',lx,'curLx',curLx,'logNamelist',logNamelist,'d1',d1,'d2',d2,'tDepth',tDepth)
            if i == (total_qx - 1) or jh != curJH or lx != curLx or (
                    tDepth[0] != d1 or tDepth[1] != d2):  # 有一个新的‘井号’或者‘深度区间’，则建立一个新的文件
                if len(logNamelist) > 0:
                    # print('WriteStart',curPath + '/' + curJH + '_' + curLx + '.las')
                    toLas(curPath + '/' + curJH + '_' + curLx + '.las', curJH, tDepth, logNamelist, logDatalist)
                    # print('Write END')
                    lasCount += 1
                    # print('lasCount = %s,  write las: well = %s,  orignal file = %s, rowIndex = %s' % (
                    #    lasCount, curJH, lx, i))
                    logNamelist.clear()
                    logDatalist.clear()
                curJH = jh
                curLx = lx
                curPath = outPath + '/' + curJH
                if os.path.exists(curPath) == False:  # 每一个井建立一个子文件夹
                    os.mkdir(curPath)

                tDepth[0] = d1
                tDepth[1] = d2
                tDepth[2] = dd  # float(result[i][getColIndex('CYJG')])
                samples = int(((tDepth[1] - tDepth[0]) / tDepth[2]) + 1)

            tLog = result[i][getColIndex('ZBSJT')].read().decode('utf-8').split(' ')
            tData = np.ones(samples, dtype='float32')
            for j in range(0, min(samples, len(tLog))):
                try:
                    tData[j] = float(tLog[j].replace(' ', ''))
                except Exception as ex:
                    # print('error: =+++++++++++++++++++++++++++++', tLog[j],'================')
                    # print('+++++++++++++++++++++++++++++++++++++%s=========================='%(tLog[len(tLog)-1]))
                    tData[j] = -999.25
                    tmpErr = '[errorIndex = %s]  i = %s, well = %s, tLog[j] = %s(j=%s, samples=%s), tLog[last] = %s ' % (
                        errorIndex, i, curJH, tLog[j], j, samples, tLog[len(tLog) - 1])
                    # print('# # # ', tmpErr)
                    fwrite_logger.debug(tmpErr)
                    # fWrite.write(tmpErr + '\n')
            # print('type of tData = ', type(tData))
            # print(tLog)    # 读取BLOB字段转换成文本
            logNamelist.append(logName)
            logFieldlist.append(logName)
            # print("==" * 20)
            # print("logNameList", type(logNamelist))
            logDatalist.append(tData)
            # if i % 10 == 0:
            #    print('process = %.2f'%(i))
        toLas(outPath + '/' + curJH + '_' + curLx + '.las', curJH, tDepth, logNamelist, logDatalist)
        # print('logFieldlist is :', logFieldlist)

        # x=c.execute('select sysdate from dual')                         #使用cursor进行各种操作
        # print(x)
        # x.fetchone()
        # cursor.close()
        sys_conn.close()
        return logFieldlist


# 获取文件夹
def get_files(path):
    name_list = os.listdir(path)
    # print(name_list)
    # current_path = os.path.abspath(__file__)
    current_path = os.getcwd()  # 获取当前路径
    # father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    # father_path = os.path.abspath('')
    # path = current_path + '/' + 'newLogPG' + '/'
    pathname = "{}/{}/".format(current_path, path)
    print(pathname)
    # for name in name_list:
    #     if os.path.isdir(path + name):
    #         pass
    #     else:
    #         name_list.remove(name)
    name_list = [name for name in name_list if os.path.isdir(pathname + name)]
    return name_list, pathname


def toLas(filename, jh, tDepth, logNameList, logDataList):
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
    las.write(filename)


def save_data(res, allFieldlist, mongoclient):
    # print('columns',qx,'allFieldlist',allFieldlist)
    # qx.insert(0, 'DEPTH')
    # qx.insert(0, 'JH')
    # qx.insert(0, 'QXWJM')
    allFieldlist.insert(0, 'JH')
    allFieldlist.insert(0, 'QXWJM')

    try:
        df_res = pd.DataFrame(res, columns=allFieldlist)

        # print(df_res.columns)
        df_res.rename(columns={
            'R2.5': 'R2_5',
            'R1.0': 'R1_0'
        }, inplace=True)

        db = mongoclient["petrol_data"]
        dbcols = db["petrol_res"]
        mongodata = df_res.to_dict(orient='records')
        print(222,mongodata[0])
        dbcols.insert(mongodata)
    except Exception as e:
        return "The error occured when processing the save data to MongoDB"
    return list(df_res.columns)


# 获取数据

# 读取result
def get_res_data(allFieldlist, outPathid, mongoclient):
    fwrite_logger = function_logger(logging.DEBUG, logging.ERROR)
    name_list, path = get_files(outPathid)
    result1 = pd.DataFrame()
    for file_path in name_list:
        # print('file_path', file_path, 'name_list', name_list)
        fwrite_logger.debug('file_path' + file_path)
        for file in os.listdir(path + '/' + file_path):
            # print('file', file)
            if file.endswith(".las"):
                jh = file.split('_')[0]
                fileext = file.split('_')[2]
                fileext = fileext.split('.')
                # print('fileext', fileext)
                qxwjm = file.split('_')[1] + '.' + fileext[0]
                # print('qxwjm', qxwjm)
                fwrite_logger.debug('qxwjm' + qxwjm)
                # print('{} 开始抽取'.format(file))
                fwrite_logger.debug('{} 开始抽取'.format(file))
                #  读取数据
                df = read_las_file(path, file_path, file)
                df['JH'] = jh
                df['QXWJM'] = qxwjm
                df = df.reset_index()
                if 'DEPTH:1' in df.columns.values.tolist():
                    df['DEPTH'] = df['DEPTH:1']
                    df = df.drop('DEPTH:1', axis=1)
                    df = df.drop('DEPTH:2', axis=1)
                    # print('{} 抽取结束'.format(file))
                    fwrite_logger.debug('{} 抽取结束'.format(file))
                result1 = result1.append(df)
    # 保存文件
    # print('result1', result1)

    pandasinfo = save_data(result1, allFieldlist, mongoclient)
    fwrite_logger.debug(pandasinfo)


'''
tDepth[start, end, step]
'''


# 读取las数据
def read_las_file(path, file_path, file):
    path = path + '/' + file_path + '/' + file
    las = lasio.read(path)
    s = time.time()
    df = las.df()
    print(time.time() - s)
    return df


if __name__ == '__main__':
    outPathid = str(uuid.uuid4())

    clientconn = get_mongoConn()
    db = clientconn["petrol_data"]
    dbcols = db["petrol_res"]
    jh = "毛坝3"
    qxwjm = "毛坝3C组合二次中完.txt"
    document = dbcols.find_one({'JH': jh, 'QXWJM': qxwjm})
    print(bool(document))
    document = {}
    print(bool(document))

    clientconn.close()
    # if os.path.exists(outPathid) == False :
    #     os.mkdir(outPathid)
    #
    # url = "puguang/puguang@192.168.43.22:1521/ORCL"
    #
    # # print(url)
    # jh = "毛坝3"
    # qxwjm = "毛坝3C组合二次中完.txt"
    # dbjob = Dbjob(url, jh, qxwjm, outPathid)
    # allFieldlist = dbjob.writeLog()
    # get_res_data(allFieldlist, outPathid)
    # shutil.rmtree(outPathid)
