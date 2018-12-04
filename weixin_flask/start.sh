#!/bin/bash
/usr/local/wx/venv/bin/gunicorn -c /usr/local/wx/weixin_flask/gun_config.py wsgi:app
