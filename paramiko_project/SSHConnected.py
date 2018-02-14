#coding=utf-8
#
import copy, re, socket
import paramiko
from paramiko import SSHException, AuthenticationException, BadHostKeyException

RUNCOMMAND_RESULT_TEMPLATE = {
    "ret": 0,
    "info": 'Default info',
    "error": None,
    "data": {
        "cmd_return": None,
    },
}

class SSHConnected(object):
    def __init__(self, host, port=22):
        self.host = str(host)
        self.port = int(port)
        self._trans = paramiko.Transport((self.host, self.port))

    def login_with_rsa(self, username, password):
        self.login_user = str(username)
        self.password=str(password)
        # self._privkey_file = str(keypath)
        # priv_key = paramiko.RSAKey.from_private_key_file(self._privkey_file)
        try:
            self._trans.connect(username=self.login_user, password=self.password)
            self._session = paramiko.SSHClient()
            self._session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._session._transport = self._trans
            return True
        except BadHostKeyException,e:
            print ">> Fail to verify the host key"
            return False
        except AuthenticationException, e:
            print ">> Fail to auth {0}@{1}:{2}".format(self.login_user, self.host, self.port)
            return False

    def close(self):
        try:
            self._trans.close()
        except Exception, e:
            return False            
        else:
            return True
    
    @property
    def closed(self):
        return not self._trans.is_active()

    @property
    def authed(self):
        return self._trans.is_authenticated()

    def run_a_command(self, cmd, env=None):
        pass

    # exec cmd in a pseudo-terminal
    def run_in_shell(self, cmd):
        self.lastcmd = str(cmd)
        self.result = copy.deepcopy(RUNCOMMAND_RESULT_TEMPLATE)
        eof = re.compile("\[.*@.*~\](\$|\#)")
        try:
            self._shell = self._session.invoke_shell()
            self._shell.settimeout(10)
            # clear login text
            self._shell.recv(65535)
            # send cmd text
            self._shell.send(self.lastcmd)
            # clear cmd text
            self._shell.recv(65535)
            # exec the cmd
            self._shell.send('\n')
            while True:
                try:
                    resp = self._shell.recv(65535)
                    resp_formated = resp.decode('utf-8').strip()
                    if eof.search(resp_formated):
                        temp = resp_formated.replace(eof.search(resp_formated).group(), '').strip()
                        self.result['ret'] = 1
                        self.result['info'] = "Success to run command \'{0}\'".format(self.lastcmd)
                        self.result['data']['cmd_return'] = temp
                        break
                    else:
                        continue
                except socket.error, e:
                    break
            # return success result
            return self.result
        except SSHException, e:
            print ">> Fail to run command \'{0}\'".format(self.lastcmd)
            self.result['info'] = "Fail to run command \'{0}\'".format(self.lastcmd)
            self.result['error'] = "Fail to run command \'{0}\'".format(self.lastcmd)
            return self.result
        finally:
            self._shell.close()

if __name__ == '__main__':
    s=SSHConnected('10.70.61.97')
    s.login_with_rsa('taojun', 'ws00310976')
    print s.run_in_shell('ls')
