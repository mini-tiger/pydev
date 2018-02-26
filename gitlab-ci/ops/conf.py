#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
from jinja2 import Template
from sys import argv
from multiprocessing import cpu_count
import os

from jinja2 import Environment, FileSystemLoader

def build_conf(ifile,ofile,k):
	env = Environment(
		loader =FileSystemLoader('.')
		)
	template = env.get_template(ifile) 
	s=template.render(k)
	print k
	print s
	with open(ofile,'wb') as f:
		f.write(s)
def init_dict(**w):

	return w

def clean_file(f):
	if os.path.isfile(f):
		os.remove(f)

if __name__ == "__main__":
	ifile=argv[2]
	ofile=argv[3]
	ttype=argv[1]
	clean_file(ofile)
	if ttype == 'config.ini':
		build_conf(ifile,ofile,init_dict(db_dev_name=argv[4],db_dev_host=argv[5],db_dev_port=argv[6],db_dev_user=argv[7],db_dev_passwd=argv[8]))
	if ttype == 'nginx':
		build_conf(ifile,ofile,init_dict(process_num=cpu_count(),static_url=argv[4]))
	if ttype == 'pip':
		build_conf(ifile, ofile, init_dict(pip_url=argv[4]))
	if ttype == 'gunicorn':
		build_conf(ifile, ofile, init_dict(chdir=argv[4],workers=cpu_count() * 2))



