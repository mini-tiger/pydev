# coding:utf-8

from __future__ import absolute_import
import socket  # 导入 socket 模块
import time


class First_socket_server(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'inst'):
            cls.inst = super(
                First_socket_server,
                cls).__new__(
                cls,
                *args,
                **kwargs)
        return cls.inst

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect(self):
        try:
            self.s = socket.socket(socket.AF_INET)  # 创建 socket 对象
            # host = socket.gethostname() # 获取本地主机名
            self.s.bind((self.ip, self.port))  # 绑定端口

            self.s.listen(1)  # 等待客户端连接

            self.c, self.addr = self.s.accept()  # 建立客户端连接。
            self.main()
        except socket.error as e:
            print e

    def close_connect(self):

        self.s.close()  # 关闭连接

    def main(self):
        n = 0
        while True:
            try:
                n += 1
                data = self.c.recv(1024)
                print '接收数据', data
                if self.addr[0] == self.ip:
                    data = '欢迎访问菜鸟教程！,这是第 {} 次'.format(n)
                    print '发送数据', data
                    self.c.sendall(data)
                    time.sleep(2)
                else:
                    self.c.close()  # 关闭连接
            except socket.error as e:
                if e.errno == 10054:
                    print 'client downline'
                    time.sleep(2)
                    self.connect()



if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 12345

    sss = First_socket_server(HOST, PORT)
    sss.connect()
