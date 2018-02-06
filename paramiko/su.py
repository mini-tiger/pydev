# coding: utf-8

import paramiko
import re
from time import sleep

# 定义一个类，表示一台远端linux主机
class Linux(object):
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
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                # 如果没有抛出异常说明连接成功，直接返回
                print u'connect %s sucess' % self.ip
                # 接收到的网络数据解码为str
                print self.chan.recv(65535).decode('utf-8')
                return
            # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
            except Exception, e1:
                if self.try_times != 0:
                    print u'连接%s失败，进行重试' %self.ip
                    self.try_times -= 1
                else:
                    print u'重试3次失败，结束程序'
                    exit(1)

    # 断开连接
    def close(self):
        self.chan.close()
        self.t.close()

    # 发送要执行的命令
    def send(self, cmd):
        # cmd += '\r'
        # 通过命令执行提示符来判断命令是否执行完成
        # p = re.compile(r'sudo.*taojun:')

        result = ''
        # 发送要执行的命令
        # self.chan.send('ws00310976'+'\n')
        while True:
            sleep(0.5)
            ret = self.chan.recv(65535)  ##注意这里是 清空ret
            # ret = ret.decode('utf-8')
            # print result

            if re.search(r'.*sudo.*for taojun:',ret):
                self.chan.send('ws00310976'+'\n')
                print ret

            if re.search(r'.*root.*',ret):

                break
        sleep(0.5)
        self.chan.send('ls -l'+'\n')
        while True:
            sleep(0.5)
            ret = self.chan.recv(65535)


            if re.search(r'root@',ret):
                self.chan.send('ls -l'+'\n')
                print ret.decode("utf-8")



if __name__ == '__main__':
    host = Linux('10.70.61.97', 'taojun', 'ws00310976')
    host.connect()
    host.send('ls -l')
    host.close()