# coding:utf-8

import cx_Oracle
from cx_Oracle import DatabaseError
import copy
from resp_template import SQL_RESULT_TEMPLATE


class util_sql(object):
	def __init__(self, ip, port, SID):

		self.dsn = cx_Oracle.makedsn(ip, port, SID)

	def main(self):
		try:
			self.conn = cx_Oracle.connect('sys', 'oracle', self.dsn, mode=cx_Oracle.SYSDBA)

			self.cursor = self.conn.cursor()
			info='Success to oracle connect ,dsn: %s' %self.dsn

			return self._retrun_dict(info=info)

		except DatabaseError as e:
			info='Fail to oracle connect ,dsn: %s' %self.dsn
			return self._retrun_dict(info=info,error=str(e))

	@staticmethod
	def _retrun_dict(info,error=None,ret=0,sql_result=None,DDL=False):

		result = copy.deepcopy(SQL_RESULT_TEMPLATE)
		result['ret'] = ret
		result['info'] = info
		result['error'] = error
		result['sql_result']['return'] = sql_result
		result['sql_result']['DDL'] = DDL

		return result


	def close_session(self):
		self.cursor.close()
		self.conn.close()


	def exec_sql(self, sql):
		try:
			self.cursor.parse(str(sql))  # 验证sql,str 防止 unicode

		except DatabaseError as e:
			info='Fail to sql verify ,sql: %s' %sql
			return self._retrun_dict(info=info,error=str(e))

		try:
			result = self.cursor.execute(sql)

			if result != None:
				info='Success to exec sql  ,sql: %s' %sql
				return self._retrun_dict(ret=1,info=info,sql_result=result.fetchall())

			else:
				info='Success to exec DDL sql  ,sql: %s' %sql
				return self._retrun_dict(ret=1,info=info,sql_result=result,DDL=True)

		except  Exception as e:
			info='Fail to exec sql  ,sql: %s' %sql
			return self._retrun_dict(info=info,error=str(e))



if __name__ == "__main__":
	s=util_sql("10.70.61.97","1521","XE")
	r=s.main()
	if r.get('error'):
		print r.get('error')
		exit(0)


	r=s.exec_sql("select * from v$database;")


	if r.get('ret'):
		print r.get('sql_result')
	else:
		print r.get('error')



	s.close_session()

