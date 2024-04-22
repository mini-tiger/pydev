#!/bin/bash
#rm -f zhongzi.tar && DOCKER_BUILDKIT=1 docker build -f deploy/docker/Dockerfile_uwsgi . --target python --tag ai/test:zhongzi --progress=plain
#rm -f zhongzi.tar && docker save  -o zhongzi.tar ai/test:zhongzi &&  scp zhongzi.tar root@172.16.157.242:/tmp/
docker stop ai-frontend-legal-web && docker rm ai-frontend-legal-web

docker-compose  -f deploy/docker/docker-compose-legal.yml up -d
