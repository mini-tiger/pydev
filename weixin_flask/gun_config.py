# -*- coding:UTF-8 -*-
from multiprocessing import cpu_count
import os


bind = '0.0.0.0:8080'
daemon = True
workers = cpu_count() * 2
threads = 2
chdir = os.path.dirname(os.path.abspath(__file__))  ##注意目录
backlog = 2048
worker_class = "gevent"  # sync, gevent,meinheld
debug = True
# proc_name='/tmp/gunicorn.pid'
pidfile = '/tmp/gunicorn.pid'
loglevel = 'debug'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = '/tmp/gunicorn_access.log'
errorlog = '/tmp/gunicorn_err.log'
raw_env = ["FLASK_CONFIG=default"]  ##环境变量
