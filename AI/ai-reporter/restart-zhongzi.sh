#!/bin/bash
#rm -f zhongzi.tar && DOCKER_BUILDKIT=1 docker build -f deploy/docker/Dockerfile_uwsgi . --target python --tag ai/test:zhongzi --progress=plain
#rm -f zhongzi.tar && docker save  -o zhongzi.tar ai/test:zhongzi &&  scp zhongzi.tar root@172.16.157.242:/tmp/
docker stop ai-flask-backend-zz && docker rm ai-flask-backend-zz
docker stop ai-frontend-web-zz && docker rm ai-frontend-web-zz
docker stop ai-frontend-mobile-zz && docker rm ai-frontend-mobile-zz
docker rmi ai/test:zhongzi
DOCKER_BUILDKIT=1 docker build -f deploy/docker/Dockerfile_uwsgi . --target python --tag ai/test:zhongzi --progress=plain
docker-compose -f deploy/docker/docker-compose-zhongzi.yml up -d