# coding=utf-8
from __future__ import absolute_import
from flask import Blueprint

monitor_bp = Blueprint("monitor_bp", __name__,
                       template_folder='template',
                       # url_prefix = '/monitor',
                       # static_folder="static"
                       )

from bk_site.monitor import error, views
