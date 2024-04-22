# syntax = docker/dockerfile:experimental
# DOCKER_BUILDKIT=1 docker build . --target python --tag ai/test:beta --progress=plain
FROM python:3.10.13-bullseye as python

RUN rm -f /etc/localtime \
&& ln -sv /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
&& echo "Asia/Shanghai" > /etc/timezone

COPY webapi/requirements.txt /tmp

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --root-user-action=ignore --disable-pip-version-check

COPY . /data/ai-reporter/
WORKDIR /data/ai-reporter

CMD [ "./start.sh" ]