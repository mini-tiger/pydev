# coding:utf-8
from __future__ import unicode_literals
from sqlalchemy.exc import *
import logging
LOG = logging.getLogger(__name__)

class MysqlUtils(object):
	def __init__(self, db):
		self.db = db

	def db_insert(self, db_cls, **kwargs):
		LOG.debug("insert data")

		db_instance = db_cls(**kwargs)

		try:
			# 将用户添加到数据库会话中
			self.db.session.add(db_instance)

			# 将数据库会话中的变动提交到数据库中,如果不Commit,数据库中是没有改动的
			self.db.session.commit()
			return db_instance
		except IntegrityError:
			self.rollback()
			LOG.debug("唯一索引冲突")
			return False
		except OperationalError:
			LOG.debug("db connection fail")
			return False
		except Exception as e:
			self.rollback()
			LOG.debug(str(e))
			return False

	def rollback(self):
		self.db.session.rollback()