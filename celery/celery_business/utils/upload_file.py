#coding=utf-8
#
from __future__ import unicode_literals
import copy
import paramiko
from paramiko import SSHException, AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError, AuthenticationException
from socket import timeout
import os
from bash_pxssh import run_script
from agent_configfile import Init_config
import logging
LOG = logging.getLogger(__name__)

RUNCOMMAND_RESULT_TEMPLATE = {
    "ret": 0,
    "info": 'Default info',
    "error": None,
    "data": {
        "cmd_return": None,
    },
}

import paramiko
class Upload_file(object):
	def __init__(self,ip=None, port=22, username=None, passwd=None, timeout=10 , os_type=None, *kw):
		self.ip= ip
		self.username = username
		self.passwd = passwd
		self.port = port
		self.kw=kw
		self.timeout = timeout
		self.os_type = os_type

	def check_channel(self):
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(self.ip, self.port, self.username, self.passwd, timeout=self.timeout)
			stdin, stdout, stderr = ssh.exec_command("ls /")
			# print stdout.readlines()
			ssh.close()
		except NoValidConnectionsError:
			return self.result_init(ret=1, info="链接失败", error="NoValidConnectionsError")
		except AuthenticationException:
			return self.result_init(ret=1,info="认证失败",error="AuthenticationException")
		except timeout:
			return self.result_init(ret=1,info="链接超时",error="socket.timeout")
		except Exception as e:
			return self.result_init(ret=1,info="失败", error=str(e))

	def result_init(self, ret=None, info=None, error=None, cmd_return=None ):
		result = copy.deepcopy(RUNCOMMAND_RESULT_TEMPLATE)
		result['ret'] = ret
		result['info'] = "host_ip: %s,detail: %s " %(self.ip,info)
		result['error'] = error
		result['data']['cmd_return'] = cmd_return if not ret else None
		return result

	def check_file(self, file):
		if not os.path.exists(file):
			return self.result_init(ret=1, info="源文件不存在", error="not file %s" %file)

	def main(self, run=False, **kw):
		# 检查是否联通
		check_result = self.check_channel()
		if check_result:
			return check_result

		if self.os_type == "linux":
			# 上传文件
			_ret_upload_file = self.upload_file_linux(**kw)
			if _ret_upload_file['ret'] == 0:
				LOG.debug("upload file %s success" %kw.get('destfile'))
				if run:
					_ret_run = run_script.run(ip=self.ip, username=self.username,
								passwd=self.passwd, script=self.destfile_fullname, run=run)
					_ret_run = _ret_run.strip()
					if _ret_run == "0":
						return self.result_init(ret=0, info="run_script: %s success" %self.destfile_fullname, error=None)
					else:
						return self.result_init(ret=1, info="Fail", error=_ret_run)
				else:
					return _ret_upload_file
			else:
				return _ret_upload_file
			

	def agent_config_upload(self, server_ip=None, destdir=None, destfile=None ,**kw):

		# init agent configfile
		cfgfile = kw.get('cfgfile')
		Init_config.agent_config_gen(tmpl_file=kw.get('tmpl_file'),
									 cfgfile=cfgfile,
									 hbs_ip=server_ip,
									 transfer_ip=server_ip)
		return self.upload_file_linux(srcfile=cfgfile, destdir=destdir, destfile=destfile)

	def upload_file_linux(self, srcfile, destdir, destfile, **kw):
		try:
			check_file = self.check_file(srcfile)
			if check_file:
				return check_file

			t = paramiko.Transport((self.ip, self.port))
			t.connect(username=self.username, password = self.passwd)
			sftp = paramiko.SFTPClient.from_transport(t)
			try:
				sftp.mkdir(destdir)
			except IOError:
				pass

			self.destfile_fullname = os.path.join(destdir, destfile).replace("\\", "/")
			sftp.put(srcfile, self.destfile_fullname)
			return self.result_init(ret=0, info="上传文件成功",error=None)
		except Exception as e:
			t.close()
			return self.result_init(ret=1,info="上传文件失败",error=str(e))


if __name__ == '__main__':
	server_ip = "192.168.43.11"
	ip="192.168.43.12"
	username = "root"
	passwd = "root"
	port = 22
	cwd_dir = os.path.dirname(os.path.abspath(__file__))
	father_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
	agent_workdir= "/tmp/install_agent"

	s = Upload_file(ip, port, username, passwd, os_type="linux")
	# upload tar.gz
	print s.main(srcfile=os.path.join(cwd_dir,'agent-0.21.tar.gz'),
				 destdir=agent_workdir,
				 destfile='agent-0.21.tar.gz',
				 run=False)
	# upload install.sh
	print s.main(srcfile=os.path.join(cwd_dir,"install.sh"),
				 destdir=agent_workdir,
				 destfile='install.sh',
				 run=False)

	print s.agent_config_upload(server_ip=server_ip,
								tmpl_file=os.path.join(cwd_dir, 'agent_config_tmpl.json'),
								cfgfile=os.path.join(cwd_dir, 'cfg.json_%s' % ip),
								destdir=agent_workdir,
								destfile='cfg.json' )
