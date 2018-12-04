# coding: utf-8
import platform
from business.Exception import *
import os
import socket

class baseconfig(object):
	CSRF_ENABLED = True

	# mail
	MAIL_SERVER = 'smtp.sina.com'
	MAIL_PROT = 25
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = "taojun319@sina.com"
	MAIL_PASSWORD = "123.com"
	# MAIL_DEBUG = True
	MAIL_DEFAULT_SENDER = 'taojun319@sina.com'


	sToken = "weixin"
	sEncodingAESKey = "BQptm8SueWbIj8z1NRPNSxdznzSAmRMiP54cKSmCsQh"
	sCorpID = "wx0a5e0ea42d34d2e1"

	# alarms_dbname = "alarms"
	# db_username = "falcon"
	# db_password = "123456"

	# db_ip = "192.168.1.108"
	# db_ip = "192.168.43.11"

	# rrd config
	# server_ip = "192.168.43.11"
	# server_ip = "192.168.1.108"
	# api_ip = "192.168.43.11" # todo api ip
	system_type = 'Windows' if platform.system().find("Win") != -1 else 'Linux'
	# redis_ip = "192.168.1.107"
	# redis_ip = "192.168.43.11"
	# redis_port = 6379
	#
	# session_config = {'SESSION_TYPE': "redis",
	# 				  'SESSION_REDIS': redis.Redis(host=redis_ip, port=redis_port, db=1, socket_connect_timeout=5),
	# 				  'SESSION_USE_SIGNER': True,
	# 				  'SECRET_KEY' : os.environ.get("SECRET_KEY", "secret-key")}
	#
	# SQLALCHEMY_BINDS = {
	# 	'falcon_portal':  'mysql://%s:%s@%s/%s' % (db_username, db_password, db_ip, 'falcon_portal')
	# }
	#
	# SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (db_username, db_password, db_ip, alarms_dbname)


	@staticmethod
	def init_app(app):
		pass


class developconfig(baseconfig):
	DEBUG = True
	# db
	# SQLALCHEMY_DATABASE_URI = 'mysql://flask:123456@192.168.31.185/flask_project'
	# SQLALCHEMY_POOL_TIMEOUT = 10
	# SQLALCHEMY_TRACK_MODIFICATIONS = False
	# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	import os
	# basedir= os.path.abspath(os.path.dirname(__file__))
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.sqlit')

	basedir = os.path.abspath(os.path.dirname(__file__))

	# SQLALCHEMY_MAX_OVERFLOW = 50
	# SQLALCHEMY_ECHO = False
	# SQLALCHEMY_POOL_SIZE = 20
	# SQLALCHEMY_TRACK_MODIFICATIONS = False
	# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	# SQLALCHEMY_POOL_TIMEOUT = 3
	# SQLALCHEMY_POOL_RECYCLE = 1


class portal(baseconfig):
	# db
	SQLALCHEMY_DATABASE_URI = 'mysql://flask:123456@192.168.31.185/flask_portal'
	SQLALCHEMY_POOL_TIMEOUT = 10
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True


config = {'default': developconfig, 'portal': portal, 'develop': developconfig}



# 定义三种日志输出格式 开始

standard_format = '[%(asctime) -s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
				  '[%(levelname)s][%(message)s]'

simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

# 定义日志输出格式 结束

logfile_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'log')  # log文件的目录

logfile_name = 'flask.log'
# 如果不存在定义的日志目录就创建一个
if not os.path.isdir(logfile_dir):
	os.mkdir(logfile_dir)

# log文件的全路径
logfile_path = os.path.join(logfile_dir, logfile_name)

# log配置字典
LOGGING_DIC = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'standard': {
			'format': standard_format,
			'datefmt': '%Y-%m-%d %H:%M:%S',
		},
		'simple': {
			'format': simple_format
		},
	},
	'filters': {},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',  # 打印到屏幕
			'formatter': 'simple'
		},
		'default': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
			'filename': logfile_path,  # 日志文件
			'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
			'backupCount': 5,
			'formatter': 'standard',
			'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
		},
	},
	'loggers': {
		'': {
			'handlers': ['default', 'console'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
			'level': 'DEBUG',
			'propagate': True,  # 向上（更高level的logger）传递
		},
	},
}
