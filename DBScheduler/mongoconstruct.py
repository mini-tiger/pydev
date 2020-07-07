import cx_Oracle
import pymongo
import pymysql
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
url = "puguang/puguang@192.168.43.22:1521/ORCL"

field_raw = [
    'JH', 'JT', 'QXWJM',
    'ZBMC', 'KC', 'CJXMID',
    'CYJG', 'YXJDDJSD1', 'YXJDDJSD2',
    'BZ', 'LRSJ', 'VRUSERNAME', 'VRUNITNAME',
    'COLLECT_JOB_S', 'GL_UUID', 'DATASTATUS', 'CJLX',
    'ORDERTIME', 'UPLOADFLAG'
]

field_crud_dict = [
    "type",
    "label",
    "value",
    "sort",
    "remarks"
]

field_crud_field = [
    "table_id",
    "field_id",
    "field_name",
    "field_type",
    "input_type",
    "relation_data",
    "default_value",
    "required_filter",
    "required_display",
    "display_sort",
    "required_input"
    "unique_index",
    "input_format",
    "display"
]

field_crud_office = [
    "id",
    "name",
    "short_name",
    "status",
    "parent",
    "type",
    "address",
    "geo",
    "remarks"
]
field_crud_table =[
    "table_id",
    "table_name"
]
field_crud_user = [
    "login_user",
    "password",
    "name",
    "status",
    "avatar",
    "gender",
    "phone",
    "email",
    "role",
    "office",
    "description",
    "birthday",
    "auth"
]
field_model_config = [
    "id",
    "modeurl",
    "inparamslist",
    "outparamslist",
    "model_name",
    "model_desc",
    "status"
]
field_oil_field_config=[
    "yqtbm",
    "yqtmc",
    "source_type",
    "conn_params"
]
field_task = [
    "taskid",
    "tasktitle",
    "taskdec",
    "status",
    "yqtbm",
    "wellname",
    "qxwjm_List",
    "model_id",
    "createBy",
    "updateBy",
    "createTime",
    "updateTime",
    "finishTime",
    "result"
]

def nosql_write(linkstr, field_list):


    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["petrol_data"]
    dbcols = db["petrol_raw"]

    sys_conn = cx_Oracle.connect(linkstr)
    cursor = sys_conn.cursor()  # 获取cursor
    sqlStr = '''SELECT JH, JT, 
    QXWJM, ZBMC, KC, CJXMID, CYJG, YXJDDJSD1,
     YXJDDJSD2, BZ, LRSJ, VRUSERNAME, VRUNITNAME，
     COLLECT_JOB_S，GL_UUID， DATASTATUS， CJLX,
     ORDERTIME, UPLOADFLAG
      from WL18'''
    # sqlStr= '''
    #     select * from WL18 where 1 = 0
    # '''
    #
    # cursor.execute(sqlStr.encode('utf-8'))
    # desc = cursor.description
    # field_list = list(filter(lambda onedesc: onedesc[1] != cx_Oracle.BLOB, desc))
    # print(field_list)
    # sqlStr = '''SELECT *
    #  from WL18'''
    # cursor.execute(sqlStr.encode('utf-8'))
    # result = cursor.fetchall()

    # for row in result:
    #     print(type(row[0]), type(row[1]))
    cursor.execute(sqlStr.encode('utf-8'))

    result = cursor.fetchall()
    for row in result:
        dictionary = dict(zip(field_list,list(row)))
        print(dictionary)
        dbcols.insert_one(dictionary)

    sys_conn.close()
def nosql_construct():

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient["petrol_data"]
    dbcols = db["crud_dict"]

    mysqldb = pymysql.connect(host='192.168.40.111',
                                user='root',
                                password='W3b5Ev!c3',
                                database='petrol_data'
                                )
    cursor = mysqldb.cursor()
    sqlstr = "select type, label, value, sort , remarks from petrol_data.crud_dict;"
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    for row in result:
        dictionary = dict(zip(field_crud_dict, list(row)))
        print(dictionary)
        dbcols.insert_one(dictionary)

    dbcols = db["crud_field"]
    sqlstr ="""select table_id, field_id, field_name, field_type, input_type, relation_data, default_value, required_filter, required_display,
    display_sort,required_input,unique_index, input_format, display from petrol_data.crud_field"""
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    for row in result:
        dictionary = dict(zip(field_crud_field, list(row)))
        print(dictionary)
        dbcols.insert_one(dictionary)

    dbcols = db["crud_office"]
    sqlstr = """select id,name,short_name,status,parent,type,address,geo,remarks from petrol_data.crud_office;"""
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    for row in result:
        dictionary = dict(zip(field_crud_office, list(row)))
        print(dictionary)
        dbcols.insert_one(dictionary)

    dbcols = db["crud_table"]
    sqlstr= """ select table_id,table_name from petrol_data.crud_table"""
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    for row in result:
        dictionary = dict(zip(field_crud_table, list(row)))
        print(dictionary)
        dbcols.insert_one(dictionary)

    dbcols = db["crud_user"]
    sqlstr=""" select login_user,password,name,
    status,avatar,gender,phone,email,role,office,
    description,birthday,auth from petrol_data.crud_user;   """
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    for row in result:
        dictionary = dict(zip(field_crud_user, list(row)))
        print(dictionary)
        dbcols.insert_one(dictionary)

    dbcols = db["model_config"]
    sqlstr="""select id,modelurl,inparamslist,outparamslist,model_name,model_desc,status from petrol_data.model_config"""
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    for row in result:
        dictionary = dict(zip(field_model_config, list(row)))
        print(dictionary)
        dbcols.insert_one(dictionary)

    dbcols = db["oil_field_config"]
    sqlstr="""select yqtbm,yqtmc,source_type,conn_params from petrol_data.oil_field_config"""
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    for row in result:
        dictionary = dict(zip(field_oil_field_config, list(row)))
        print(dictionary)
        dbcols.insert_one(dictionary)

    dbcols = db["task"]
    sqlstr = """ select taskid,tasktitle,taskdesc,status,
                yqtbm,wellname,qxwjm_List,model_id,
                createBy,updateBy,createTime,updateTime,finishTime,
                result from petrol_data.task """
    cursor.execute(sqlstr)
    result = cursor.fetchall()
    for row in result:
        dictionary = dict(zip(field_task, list(row)))
        print(dictionary)
        dbcols.insert_one(dictionary)
if __name__ == "__main__":
    #nosql_write(url)
    nosql_construct()