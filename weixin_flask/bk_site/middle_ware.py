# coding:utf-8
import logging
LOG = logging.getLogger(__name__)
from flask import g, request, redirect, session
from rrd.view.utils import get_usertoken_from_session, get_current_user_profile
from monitor import monitor_bp
from rrd import config
from business.Exception import *

def app_before(app):
	@monitor_bp.before_request  # monitor_bp 蓝本请求走此方法
	# @app.before_request   不使用app , other_bp 现不需要判断
	def request_before():
		if session:
			g.user_token = get_usertoken_from_session(session)
			g.user = get_current_user_profile(g.user_token)
			g.locale = request.accept_languages.best_match(config.LANGUAGES.keys())
			if not g.user:
				return redirect("/auth/login")
		# 	# print ut
		# 	current_app.login_type = 1
		# 	current_app.user = g.user_token.name
		# 	current_app.sig = g.user_token.sig
		# 	g.user = get_current_user_profile(g.user_token)
		# 	g.locale = request.accept_languages.best_match(config.LANGUAGES.keys())
		else:
			return redirect("/auth/login")
		# 	if getattr(current_app, 'login_type', 0):
		# 		ut = user.UserToken(current_app.user, current_app.sig)
		# 		set_user_cookie(ut, session)
		# 	else:
		#

		path = request.path
		# if path.startswith("/mail"):
		# 	print dir(request)
		# 	print request.host
		# 	print request.host_url
		# 	print request.remote_addr
		# 	return
		# if not g.user:
		# 	return redirect("/auth/login")
		LOG.debug("Middle_Ware func IP: %s ,user: %s,url: %s" % (request.remote_addr, request.remote_user, request.base_url))
	# return request_before
