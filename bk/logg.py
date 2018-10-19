# -*- coding: utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler
import os


class log_class(object):
	def __init__(self, logger):
		self.log = logging.getLogger(logger)
		formatter = logging.Formatter('%(asctime)s %(levelname)-5s %(message)s')  # 每行日志的前缀设置
		fileTimeHandler = TimedRotatingFileHandler(filename=os.path.join(os.getcwd(), "run.log"), when="D", interval=1,
												   backupCount=7)
		fileTimeHandler.suffix = "%Y%m%d"  # 设置 切分后日志文件名的时间格式 默认 filename+"." + suffix 如果需要更改需要改logging 源码
		fileTimeHandler.setFormatter(formatter)
		# logging.basicConfig(level=logging.DEBUG)
		fileTimeHandler.setFormatter(formatter)
		self.log.level=logging.DEBUG
		self.log.addHandler(fileTimeHandler)

	def info(self, message):
		print (message)
		self.log.info(message)

	def error(self, message):
		print (message)
		self.log.error(message)

	def debug(self, message):
		print (message)
		self.log.debug(message)
