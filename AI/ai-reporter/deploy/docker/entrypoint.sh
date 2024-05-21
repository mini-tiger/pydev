#!/bin/bash
source /etc/profile

unset ALL_PROXY && unset http_proxy && unset HTTP_PROXY && unset HTTPS_PROXY && unset https_proxy
env

cd /data/ai-reporter/ || exit

# 用环境变量的值替换模板中的占位符，生成实际的配置文件
envsubst < /data/ai-reporter/deploy/docker/app.nginx.template > /etc/nginx/sites-available/app && ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
nginx -t && service nginx start

cp /data/ai-reporter/deploy/docker/*.docx  /data/ai-reporter/webapi/app/attachments/
uwsgi -i deploy/docker/app.ini