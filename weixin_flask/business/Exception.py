#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from exceptions import BaseException, Exception

class Bk_site_exception(Exception):
		pass


class Redis_timeout_err(Bk_site_exception):
	def __init__(self, err="redis connection timeout"):
		Bk_site_exception.__init__(self, err)


class Redis_connect_err(Bk_site_exception):
	def __init__(self, err="redis connection err"):
		Bk_site_exception.__init__(self, err)