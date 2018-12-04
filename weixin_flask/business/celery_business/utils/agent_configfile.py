#coding=utf-8
from __future__ import unicode_literals
from jinja2 import Template
import os
class Init_config(object):
	def __init__(self):
		pass

	@classmethod
	def agent_config_gen(cls,tmpl_file=None, cfgfile=None, **kw):
		with open(tmpl_file,'r') as f:
			s=f.readlines()
		ss = ''.join(s)
		template = Template(ss)  ##1
		s=template.render(hbs_ip=kw.get('hbs_ip'), transfer_ip=kw.get('transfer_ip'))

		with open(cfgfile,'w') as f:
			f.write(s)

if __name__ == "__main__":
	cwd_dir = os.path.dirname(os.path.abspath(__file__))
	utils_dir = os.path.join(cwd_dir,'utils')
	Init_config.agent_config_gen(tmpl_file=os.path.join(cwd_dir,'agent_config_tmpl.json'),
								 cfgfile=os.path.join(cwd_dir,'cfg.json'),
								 hbs_ip="192.168.43.11",
								 transfer_ip="192.168.43.11")
