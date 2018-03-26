# coding:utf-8

from __future__ import absolute_import
import time

# import socket               # 导入 socket 模块

# s = socket.socket()         # 创建 socket 对象
# host = socket.gethostname() # 获取本地主机名
# port = 12345                # 设置端口好

# c=s.connect(('127.0.0.1', port))
# print s.recv(1024)
# print c
# # c.send('我是client')
# s.close()
import socket
import gevent
from gevent import socket, monkey
from gevent.threadpool import ThreadPool  #同时并发

monkey.patch_all()

print dir(socket)
n = 0


class First_socket_client(object):
	# def __new__(cls, *args, **kwargs):
	#
	# 	if not hasattr(First_socket_client, 'inst'):
	# 		First_socket_client.inst = super(
	# 			First_socket_client, cls).__new__(
	# 			cls, *args, **kwargs)
	# 	return cls.inst

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port

	def connect(self,n=0):
		try:
			self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

			self.s.connect((self.ip, self.port))  # 要连接的IP与端口
		except socket.error as e:
			print e
			if e.errno == 10061:
				print 'Connect Fail , Errno : {}'.format(e)
			time.sleep(1)
			n+=1
			if n > 10:
				print 'Connect Fail , Errno : {} , Retry already 10 ,exit'.format(e)
				exit(1)
			else:
				self.connect(n)


	def recv_data(self):
		try:
			self.data = self.s.recv(1024)
			return True
		except NameError as e:
			print e
			return False

	def close_connect(self):

		self.s.close()  # 关闭连接

	def main(self):
		n=0
		while True:
			try:

				n += 1
				print '本机ip : {},port: {}'.format(self.s.getsockname()[0],self.s.getsockname()[1])
				send_data = 'This is client ,Num : {:^10}'.format(n)  # 与人交互，输入命令
				print '发送数据', send_data
				# gevent.sleep(0)
				self.s.sendall(send_data)  # 把命令发送给对端

				if self.recv_data():
					print '接收到的数据: {:^30}'.format(self.data)
				self.close_connect()
				self.connect()##重新连接
				# time.sleep(3)## 睡3 秒，一次接收3秒内的数据
			except socket.error as e:
				if 10061 == e.errno:
					print 'server 失去链接'
					# time.sleep(2)
					self.close_connect()
					self.connect()##重新连接
				if 10054 == e.errno:
					print 'server 强制断开链接'
					# time.sleep(2)
					self.close_connect()
					self.connect()##重新连接
				if 10053 == e.errno:
					# e=u'server 不接收数据'.encode('gbk')
					e = 'server 不接收数据'
					print e
					time.sleep(3)
					self.close_connect()
					self.connect()


if __name__ == '__main__':
	HOST = '127.0.0.1'
	PORT = 12345
	ss=First_socket_client(HOST,PORT)
	ss.connect()
	# ss.main()
	ss1=First_socket_client(HOST,PORT)
	ss1.connect()
	ss.main()
	pool = ThreadPool(2)   ##同时并发 pool是可以指定池子里面最多可以拥有多少greenlet在跑

	# for i in xrange(10):
	pool.spawn(ss.main())
	pool.spawn(ss1.main())

	pool.join()