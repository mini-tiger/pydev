#coding=utf-8
from utils.upload_file import Upload_file
from settings import baseconfig
from bk_site import celery_app as app
import os

@app.task
def upload_file_ssh(ip):
	server_ip = "192.168.43.11"
	ip="192.168.43.12"
	username = "root"
	passwd = "root"
	port = 22
	cwd_dir = os.path.dirname(os.path.abspath(__file__))
	cwd_dir = os.path.join(cwd_dir,'utils')
	#father_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
	agent_workdir= "/tmp/install_agent"

	s = Upload_file(ip, port, username, passwd, os_type="linux")
	# upload tar.gz
	_ret = s.main(srcfile=os.path.join(cwd_dir,'agent-0.21.tar.gz'),
				 destdir=agent_workdir,
				 destfile='agent-0.21.tar.gz',
				  # win 关闭脚本执行
				 run=False)
	if _ret['ret'] != 0:
		return _ret

	# create agent config as  cfg.json
	_ret = s.agent_config_upload(server_ip=server_ip,
								tmpl_file=os.path.join(cwd_dir, 'agent_config_tmpl.json'),
								cfgfile=os.path.join(cwd_dir, 'cfg.json_%s' % ip),
								destdir=agent_workdir,
								destfile='cfg.json' )
	if _ret['ret'] != 0:
		return _ret

	# upload install.sh
	_ret = s.main(srcfile=os.path.join(cwd_dir,"install.sh"),
				 destdir=agent_workdir,
				 destfile='install.sh',
				 run=True if baseconfig.system_type != "Windows" else False )
	if _ret['ret'] != 0:
		return _ret

	return s.result_init(ret=0, info="task sucess", error=None)


@app.task
def taskB(x, y, z):
	return x + y + z


@app.task
def add(x, y):
	return x + y
