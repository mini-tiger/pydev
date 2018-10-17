# coding=utf-8
import re
from time import sleep
import socket
import paramiko
import platform
from uploadfile import Upload_file
from copy import deepcopy


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
    def send(self, cmd, re_str, code_type, timeout=0.1):

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


def run_cmd(cmd):
    host = util_ssh('192.168.43.14', dict_use["login_user"], dict_use["login_passwd"])
    connection = host.connect()

    if connection:
        # host.send('ps aux|grep -v grep ',"\[.*@.*\](\$|\#)") #匹配 命令行
        host.send(cmd, "\[.*@.*\](\$|\#)", dict_use["code_type"])
        # rm old dir
        host.send(cmd, "\[.*@.*\](\$|\#)", dict_use["code_type"])
        host.close()


if __name__ == "__main__":
    os_type = "Win"  # 目标机器系统类型

    dict_win = {"code_type": "gbk", "login_user": "Administrator", "login_passwd": "123.com",
                "dest_dir": "/cygdrive/c/", "dest_file": "falcon-agent_win.tar.gz"}

    dict_linux = {"code_type": "utf-8", "login_user": "root", "login_pass": "123.com",
                  "dest_dir": "/home/falcon"}

    if os_type.find("Win") != -1:
        dict_use = deepcopy(dict_win)

        cmd_kill = "taskkill /F /pid `netstat -ano | grep 7777 | awk.exe '{print $5}'` "

        cmd_rmolddir = "rm -rf %s" % (dict_use["dest_dir"] + "falcon-agent_win")

        cmd_line_addtasks = "schtasks /create /tn 'My App' /tr c:\\falcon-agent_win\\start.bat /sc onstart /ru %s /rp %s /F" % (
            dict_use["login_user"], dict_use["login_passwd"])

        # cmd_line_sendfile = "scp -r /root/falcon-agent_win/ %s@192.168.43.14:%s" % (
        #     dict_use["login_user"], dict_use["dest_dir"])
        cmd_start_falcon = "cmd.exe /c 'C:\\falcon-agent_win\\start.bat'"
        cmd_mk = "mkdir -p %s" % (dict_use["dest_dir"] + "alcon-agent_win/cfg")
        cmd_tar = "tar xf /tmp/%s -C %s" % (dict_use["dest_file"], dict_use["dest_dir"])

    else:
        dict_use = deepcopy(dict_linux)

    # 关闭旧程序
    run_cmd(cmd_kill)

    # rm old dir
    run_cmd(cmd_rmolddir)

    # mkdir
    # run_cmd(cmd_mk)

    # sendfile
    # run_cmd(cmd_line_sendfile)
    s = Upload_file('192.168.43.14', 22, dict_use["login_user"], dict_use["login_passwd"], os_type="linux")

    s.main(srcfile='/root/%s' % (dict_use["dest_file"]), destdir="/tmp/", destfile=dict_use["dest_file"], run=False)

    run_cmd(cmd_tar)
    # add tasks
    run_cmd(cmd_line_addtasks)
    # start falcon
    run_cmd(cmd_start_falcon)
