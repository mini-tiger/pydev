# coding:utf-8
from __future__ import absolute_import
from flask import render_template, redirect, url_for, request, flash, abort

from bk_site.monitor import monitor_bp

'''

from monitor_bk_site.monitor.models.models import Abc
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# # 初始化数据库连接:
# engine = create_engine('mysql+mysqlconnector://falcon:123456@192.168.31.230:3306/alarms')
# # 创建DBSession类型:
# DBSession = sessionmaker(bind=engine)
'''
# use flask_sqlalchemy
from bk_site.monitor.models.models import *
from business.mysql_utils import MysqlUtils
import logging

LOG = logging.getLogger(__name__)
############################################################
from flask import g, request
from business.utils import allow_cross_domain
from business.celery_business import tasks


@monitor_bp.route('/', methods=["GET", "POST"])
@allow_cross_domain
def index():

	'''
	# 使用sqlalchemy 弃用
	# session = DBSession()
	# # 创建新User对象:
	# new_user = Abc(a='5', b='Bob')
	# # 添加到session:
	# session.add(new_user)
	# # 提交即保存到数据库:
	# session.commit()
	# # 关闭session:
	# session.close()
	'''
	# print dir(Abc)
	# print Abc.query.all()
	# print Expression.query.first()
	# print Expression.query.first().expression
	# query_set = User.query.all()
	# print query_set
	# r=tasks.upload_file_ssh.apply_async(kwargs={"ip":1}, queue="upload_file_ssh", routing_key="upload_file_ssh")
	r = tasks.add.apply_async(args=(1, 2), queue="task_add", routing_key="task_add")
	_db = MysqlUtils(db)

	# _result = _db.db_insert(db_cls=User, name='aaaaaaa', passwd="a")
	# print _result
	import random
	i = random.randint(0, 99)
	print i
	eventcase_result = _db.db_insert(db_cls=EventCase, id=i, endpoint='dd', metric="m", cond="c", priority=1,
									 status="a")

	if eventcase_result:
		# event_result = _db.db_insert(db_cls=Event, event_case=eventcase_result, cond="c")
		event = Event(event_case=eventcase_result, cond="c")
		event_result = event.save()
		print event_result

	# 分页
	url_root = "monitor_bp.index"
	page = request.args.get('page', "1")  # 当前页
	_per_page = request.args.get("per_page", 3)  # 每页默认几条数据
	print page, _per_page
	pagination = Event.query.order_by(Event.event_caseId.desc()).paginate(int(page),
																		  per_page=int(_per_page),
																		  error_out=False)
	data = pagination.items

	# 一查多
	# print dir(event_result)
	# print event_result.event_case
	# print event_result.event_caseId
	# print Event.query.filter(EventCase.id==1).all()

	# aa = Tpl.query.first()
	# print dir(aa)
	# print aa._tpl
	# # 多查一
	# # print dir(eventcase_result)
	# print eventcase_result._EventCase[0].id
	#
	# print EventCase.query.filter(EventCase.id == 1).first()
	LOG.debug("111111111111111111")
	flash('You were logged in')

	return render_template('aa/index.html', **locals())


from flask import jsonify


@monitor_bp.route("/vue", methods=["GET", "POST"])
@allow_cross_domain
def tests_cross_domain():
	return render_template('aa/vue.html', **locals())


@monitor_bp.route('/err/', methods=["GET", "POST"])
def err():
	print 123
	abort(404, )
