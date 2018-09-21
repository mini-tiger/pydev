# coding=utf-8
import re
from time import sleep
import socket
import paramiko
import platform
from uploadfile import Upload_file

class util_ssh(object):
	# 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
	def __init__(self, ip, username, password, timeout=15):
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
				self.chan.invoke_shell()  ##在SSH server端创建一个交互式的shell，且可以按自己的需求配置伪终端，可以在invoke_shell()函数中添加参数配置
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
					print u'失败原因:' + str(e)
					return False

	# 断开连接
	def close(self):
		self.chan.close()
		self.t.close()
		return

	# 发送要执行的命令
	def send(self, cmd, re_str,  code_type, timeout=0.5):

		# cmd += '\r'
		# 通过命令执行提示符来判断命令是否执行完成
		# p = re.compile(r'sudo.*taojun:')

		# 发送要执行的命令
		# self.chan.send('ws00310976'+'\n')

		# if re.search(re_str,self._ret):
		# 	self.chan.send(cmd + '\n')

		sleep(timeout)

		try:
			while True:
				if re.search(re_str, self.chan.recv(65535)):  # 第一次  命令提示符发送命令,# 通过recv函数获取回显, 清空上一次的回显
					self.chan.send(cmd + '\n')
					break

			while True:
				sleep(timeout)
				ret = self.chan.recv(65535)
				if re.search(re_str, ret):
					ret = ret.decode(code_type)
					print ret
					break
				else:
					continue

		except socket.error as e:
			print str(e)
		# finally:
		# 	self.close()


if __name__ == "__main__":
	send_file()
	cmd_line = "schtasks /create /tn 'My App' /tr c:\\falcon-agent\\start.bat /sc onstart /ru administrator /rp 123.com /F"
	host = util_ssh('192.168.43.14', 'Administrator', '123.com')
	connection = host.connect()
	code_type = "gbk" if platform.system().find("Win") != -1 else "utf-8"

	if connection:
		# host.send('ps aux|grep -v grep ',"\[.*@.*\](\$|\#)") #匹配 命令行
		host.send(cmd_line, "\[.*@.*\](\$|\#)", code_type)
		host.close()
