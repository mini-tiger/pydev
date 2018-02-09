# coding:utf-8

import cx_Oracle
from cx_Oracle import DatabaseError
import paramiko, re
from time import sleep


class util_sql(object):
	def __init__(self, ip, port, SID):

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

class util_ssh(object):
	# 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
	def __init__(self, ip, username, password, timeout=30):
		self.ip = ip
		self.username = username
		self.password = password
		self.timeout = timeout
		# transport和chanel
		self.t = ''
		self.chan = ''
		# 链接失败的重试次数
		self.try_times = 3

	# 调用该方法连接远程主机


	def connect(self):
		while True:
			# 连接过程中可能会抛出异常，比如网络不通、链接超时
			try:
				self.t = paramiko.Transport(sock=(self.ip, 22))
				self.t.connect(username=self.username, password=self.password)
				# print self.t.is_authenticated()
				self.chan = self.t.open_session()
				self.chan.settimeout(self.timeout)
				self.chan.get_pty()
				self.chan.invoke_shell()
				# 如果没有抛出异常说明连接成功，直接返回
				print u'connect %s sucess' % self.ip
				# 接收到的网络数据解码为str
				print self.chan.recv(65535).decode('utf-8')
				return True

			except Exception as e:
				if self.try_times != 0:
					print u'连接%s失败，进行重试' % self.ip
					self.try_times -= 1
				else:
					print u'重试3次失败，结束程序'
					print u'失败原因:'+str(e)
					return False


	# 断开连接
	def close(self):
		self.chan.close()
		self.t.close()
		return

	# 发送要执行的命令
	def send(self, cmd, re_str, timeout=5):
		# cmd += '\r'
		# 通过命令执行提示符来判断命令是否执行完成
		# p = re.compile(r'sudo.*taojun:')

		result = ''
		# 发送要执行的命令
		# self.chan.send('ws00310976'+'\n')
		while True:
			self.chan.send(cmd + '\n')
			sleep(timeout)
			ret = self.chan.recv(65535)

			if re.search(re_str,ret):
				ret = ret.decode('utf-8')
				print ret
				return


if __name__ == "__main__":
	s=util_sql("10.70.61.97","1521","X")
	r=s.main()
	if r.get('code') == 0:
		print r.get('errmsg')
		exit(0)
	# else:
	# 	print r.get('result')


	r=s.exec_sql("select database_role from v$database")

	if r.get('code') == 0:

		print r.get('errmsg')
	else:
		print r.get('result')
	# print s.exec_sql("select process, pid, status, client_process, client_pid from v$managed_standby")
	s.close_session()

	# host = util_ssh('10.70.61.97', 'taojun', 'ws00310976')
	# connection=host.connect()
	# if connection:
	# 	host.send('ps aux|grep -v grep |grep sshd ','\[taojun@')
	# 	host.close()
