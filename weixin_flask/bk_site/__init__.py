# coding=utf-8
from flask import Flask
from werkzeug.utils import import_string
from settings import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    # blueprints = [
    #     # 'bk_site.monitor:monitor_bp',
    #     'bk_site.other:other_bp',
    # ]
    #
    # for bp_name in blueprints:
    #     bp = import_string(bp_name)
    #     app.register_blueprint(bp)
    from bk_site.weixin import wx_bp
    app.register_blueprint(wx_bp)
    return app
