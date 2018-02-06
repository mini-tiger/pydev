
#coding:utf-8

import cx_Oracle

dsn=cx_Oracle.makedsn("10.70.61.97","1521","XE")

conn=cx_Oracle.connect('sys','oracle',dsn,cx_Oracle.SYSDBA)

cursor = conn.cursor()

result=cursor.execute("select instance_name from v$instance")
print result.fetchall()