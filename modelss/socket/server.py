# coding:utf-8

from __future__ import absolute_import
import socket               # 导入 socket 模块
import time
s = socket.socket(socket.AF_INET)         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port = 12345                # 设置端口
s.bind(('127.0.0.1', port))        # 绑定端口

s.listen(1)                 # 等待客户端连接

c, addr = s.accept()     # 建立客户端连接。
print('连接地址：', c, addr)
n=0
while True:
    n+=1
    data=c.recv(1024)
    print '接收数据',data
    if addr[0] == '127.0.0.1':
        data='欢迎访问菜鸟教程！,这是第 {} 次'.format(n)
        print '发送数据',data
        c.sendall(data)
        time.sleep(2)
    else:
        c.close()                # 关闭连接