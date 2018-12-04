# coding=utf-8
from __future__ import absolute_import
from flask import Blueprint

wx_bp = Blueprint("wx_bp", __name__,
                      template_folder = 'template',
                      # url_prefix = '/monitor'
                       )

from bk_site.weixin import views