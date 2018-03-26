# coding:utf-8

from __future__ import absolute_import
import socket  # 导入 socket 模块
import time
import gevent
from gevent import socket, monkey

monkey.patch_all()


class First_socket_server(object):
	def __new__(cls, *args, **kwargs):
		# print args
		# print kwargs
		cls.ip = kwargs['ip']
		cls.port = kwargs['port']
		if not hasattr(cls, 'inst'):
			cls.inst = super(
				First_socket_server,
				cls).__new__(
				cls,
				*args,
				**kwargs)
		return cls.inst

	def __init__(self, ip, port):
		pass

	@classmethod
	def connect(cls):
		try:
			cls.s = socket.socket(socket.AF_INET)  # 创建 socket 对象
			# host = socket.gethostname() # 获取本地主机名
			cls.s.bind((cls.ip, cls.port))  # 绑定端口

			cls.s.listen(5000)  # 等待客户端连接
		except socket.error as e:
			print e

	@classmethod
	def connect_accept(cls):
		try:
			cls.c, cls.addr = cls.s.accept()  # 建立客户端连接。
			# gevent.joinall([gevent.spawn(cls.main)])
			# cls.main()
		except socket.error as e:
			print e

	@classmethod
	def close_connect(cls):

		cls.s.close()  # 关闭连接

	@classmethod
	def main(cls):
		n = 0
		while True:
			try:
				cls.connect_accept()
				print '远程IP: {},端口: {}'.format(cls.addr[0],cls.addr[1])
				n += 1
				data = cls.c.recv(1024)
				print '接收数据', data
				if cls.addr[0] == cls.ip:
					data = '欢迎访问菜鸟教程！,这是第 {} 次'.format(n)
					print '发送数据', data
					cls.c.sendall(data)
					time.sleep(2)
					# cls.c.close()
				else:
					pass
					# cls.c.close()  # 关闭连接
			except socket.error as e:
				print e
				if e.errno == 10054:
					print 'client downline'
					time.sleep(2)
					cls.connect()


if __name__ == '__main__':
	HOST = '127.0.0.1'
	PORT = 12345

	sss = First_socket_server(ip=HOST, port=PORT)
	sss.connect()
	gevent.spawn(sss.main())
