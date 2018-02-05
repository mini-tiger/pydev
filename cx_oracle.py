# coding:utf-8

import cx_Oracle

class init_sql(object):
	def __init__(self,ip,port,SID):
		dsn=cx_Oracle.makedsn(ip,port,SID)


		conn=cx_Oracle.connect('sys','oracle',dsn,cx_Oracle.SYSDBA,events=True)

		self.cursor = conn.cursor()

	def exec_sql(self,sql):
		try:
			result=self.cursor.execute(sql)
			print cx_Oracle.OPCODE_ALTER
			print cx_Oracle.OPCODE_UPDATE
			print cx_Oracle.OPCODE_DELETE
			print cx_Oracle.OPCODE_ALLOPS
			print result
		except  Exception as e:
			print e

if __name__ == "__main__":
	s=init_sql("10.70.61.97","1521","XE")
	s.exec_sql("select database_role,open_mode,switchover_status,flashback_on from v$database")
	s.exec_sql("alter system switch logfile")