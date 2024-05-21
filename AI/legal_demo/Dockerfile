# syntax = docker/dockerfile:experimental
# DOCKER_BUILDKIT=1 docker build . --target python --tag ai/test:beta --progress=plain
FROM python:3.10.13-bullseye as python

RUN rm -f /etc/localtime \
&& ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone

RUN --mount=type=cache,target=/root/cache/apt/archives \
    unset ALL_PROXY && unset http_proxy && unset HTTP_PROXY && unset HTTPS_PROXY && unset https_proxy \
    && sed -i 's#http://deb.debian.org#https://mirrors.huaweicloud.com#g' /etc/apt/sources.list && apt-get update &&  apt install -y libreoffice
COPY '公司差旅费管理实施细则（咨财〔2019〕2583号，2019年修订）.doc'  /data/
