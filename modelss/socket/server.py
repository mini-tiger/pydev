# coding:utf-8

from __future__ import absolute_import
import socket  # 导入 socket 模块
import time
from gevent.threadpool import ThreadPool  # 同时并发


class First_socket_server(object):
	# def __new__(cls, *args, **kwargs):
	#     if not hasattr(cls, 'inst'):
	#         cls.inst = super(
	#             First_socket_server,
	#             cls).__new__(
	#             cls,
	#             *args,
	#             **kwargs)
	#     return cls.inst

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port

	def connect(self):
		try:
			self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 创建 socket 对象
			# host = socket.gethostname() # 获取本地主机名
			self.s.bind((self.ip, self.port))  # 绑定端口

			self.s.listen(1)  # 等待客户端连接

			# self.c, self.addr = self.s.accept()  # 建立客户端连接
			# print '远程IP: {},端口: {}'.format(self.addr[0],self.addr[1])

		except socket.error as e:
			if e.errno == 10048:
				print '端口占用'
				exit(1)

	def close_connect(self):

		self.s.close()  # 关闭连接

	def main(self):
		n = 0
		while True:
			try:
				self.c, self.addr = self.s.accept()  # 建立客户端连接
				self.c.settimeout(5)

				print '远程IP: {},端口: {}'.format(self.addr[0], self.addr[1])
				n += 1
				data = self.c.recv(1024)
				print '接收数据', data
				if self.addr[0] == self.ip: ##本机
					data = '欢迎访问菜鸟教程！,这是第 {} 次'.format(n)
					print '发送数据', data
					self.c.sendall(data)
					self.c.close()
					# time.sleep(2)
				else:
					self.c.close()  # 关闭连接
				time.sleep(2)
			except socket.error as e:
				print e
				if e.errno == 10054:
					print 'client downline'
					time.sleep(2)
					self.connect()
			except socket.timeout as e:
				print e

if __name__ == '__main__':
	HOST = '127.0.0.1'
	PORT = 12345

	sss = First_socket_server(HOST, PORT)
	sss.connect()
	sss.main()

	# sss1 = First_socket_server(HOST, PORT)
	# sss1.connect()
	sss.main()
	#
	# pool = ThreadPool(2)  ##同时并发 pool是可以指定池子里面最多可以拥有多少greenlet在跑
	#
	# # for i in xrange(10):
	# pool.spawn(sss.main())
	# pool.spawn(sss.main())
	#
	# pool.join()
