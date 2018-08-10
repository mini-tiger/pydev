from pexpect import pxssh
# import getpass

class run_script(object):
    def __init__(self, timeout=10, ):
        pass

    @classmethod
    def run(cls, ip=None, username=None, passwd=None, script=None, **kw):
        try:
            session = pxssh.pxssh(timeout=10, echo=False)
            # hostname = raw_input('hostname: ')
            # username = raw_input('username: ')
            # password = getpass.getpass('password: ')
            session.force_password = True
            session.login(ip, username, passwd,login_timeout=10)
            # s.sendline('uptime')   # run a command
            # s.prompt()             # match the prompt
            # print(s.before)        # print everything before the prompt.
            session.sendline('bash %s' % script)
            session.prompt()
            ret = session.before
            session.logout()
            return ret

        except pxssh.ExceptionPxssh as e:
#            return "pxssh failed on login."
            return str(e)

if __name__ == "__main__":
    run_script.run(ip="192.168.43.12", username="root", passwd="root", script="/tmp/install_agent/install.sh")
