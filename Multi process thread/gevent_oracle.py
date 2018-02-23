# coding:utf-8
import sys

sys.path=sorted(sys.path,reverse=False)  #把当前文件夹路径，放到最后
# print sys.path

from gevent import monkey; monkey.patch_all()
import gevent
import cx_Oracle


class util_sql(object):
	def __init__(self, ip, port, SID):
		# self.ip=ip
		# self.port=port
		# self.sid=SID
		self.dsn = cx_Oracle.makedsn(ip, port, SID)

	def main(self):
		try:
			self.conn = cx_Oracle.connect('sys', 'oracle', self.dsn, mode=cx_Oracle.SYSDBA)

			self.cursor = self.conn.cursor()
			return self._retrun_dict(code=1)
		except DatabaseError as e:
			return self._retrun_dict(code=0,message=str(e))

	@staticmethod
	def _retrun_dict(code,message='',results=''):
		return {'code':code,'errmsg':message,'result':results}


	def close_session(self):
		self.conn.close()


	def exec_sql(self, sql):
		try:
			self.cursor.parse(sql)  # 验证sql

		except DatabaseError as e:
			return self._retrun_dict(code=0,message=str(e))

		try:
			result = self.cursor.execute(sql)

			if result != None:
				return self._retrun_dict(code=1,results=result.fetchall())
			else:
				return self._retrun_dict(code=1,results=result.fetchall())##DDL

		except  Exception as e:
			# print "sql : " + sql + "\n" + "exec error: " + str(e)
			return self._retrun_dict(code=0,message=str(e))

def f(sql):
	print gevent.getcurrent()
	s=util_sql("10.70.61.97","1521","XE")
	r=s.main()
	if r.get('code') == 0:
		print r.get('errmsg')
		exit(0)
	# else:
	# 	print r.get('result')


	r=s.exec_sql(sql)

	if r.get('code') == 0:

		print r.get('errmsg')
	else:
		print r.get('result')
	# print s.exec_sql("select process, pid, status, client_process, client_pid from v$managed_standby")
	s.close_session()



if __name__ == '__main__':

	gevent.joinall([
		    gevent.spawn(f, 'select database_role from v$database'),
	        gevent.spawn(f, 'select database_role from v$database'),

	])