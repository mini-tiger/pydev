# coding:utf-8

import cx_Oracle
from cx_Oracle import DatabaseError

class util_sql(object):
	def __init__(self, ip, port, SID):
		try:
			dsn = cx_Oracle.makedsn(ip, port, SID)

			self.conn = cx_Oracle.connect('sys', 'oracle', dsn, mode=cx_Oracle.SYSDBA)

			self.cursor = self.conn.cursor()
		except Exception as e:
			print e

	def close_session(self):
		self.conn.close()

	def exec_sql(self, sql):
		try:
			self.cursor.parse(sql)  # 验证sql

		except DatabaseError as e:
			# error, = e.args
			# print("Oracle-Error-Code:", error.code)
			# print("Oracle-Error-Message:", error.message)
			return {'error':True,'detail':str(e)}

		try:
			result = self.cursor.execute(sql)

			if result != None:
				return {'result':result.fetchall()[0],'error':False}
			else:
				return {'result':None,'error':False }##DDL

		except  Exception as e:
			# print "sql : " + sql + "\n" + "exec error: " + str(e)
			return {'error':True,'detail':str(e)}

if __name__ == "__main__":
	s=util_sql("10.70.61.97","1521","XE")
	r=s.exec_sql("select database_role from v$database")
	if not r.get('error',True):
		print r
	else:
		print 'error: '+r['detail']

	r=s.exec_sql("alter system switch logfile")
	if not r.get('error',True):
		print r
	else:
		print 'error: '+r['detail']

	s.close_session()