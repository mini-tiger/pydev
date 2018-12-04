from functools import wraps
from flask import make_response


def allow_cross_domain(fun):
	@wraps(fun)
	def wrapper_fun(*args, **kwargs):
		rst = make_response(fun(*args, **kwargs))
		rst.headers['Access-Control-Allow-Origin'] = '*'
		rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
		allow_headers = "Referer,Accept,Origin,User-Agent"
		rst.headers['Access-Control-Allow-Headers'] = allow_headers
		return rst

	return wrapper_fun
