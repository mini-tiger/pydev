#!/bin/bash
docker stop ai-flask-backend-5001 && docker rm ai-flask-backend-5001
docker rmi ai/test:9001
DOCKER_BUILDKIT=1 docker build -f deploy/docker/Dockerfile_uwsgi . --target python --tag ai/test:9001 --progress=plain
docker-compose -f deploy/docker/docker-compose-9001.yml up -d