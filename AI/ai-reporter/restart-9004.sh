#!/bin/bash
docker stop ai-flask-backend-5004 && docker rm ai-flask-backend-5004
docker rmi ai/test:9004
DOCKER_BUILDKIT=1 docker build -f deploy/docker/Dockerfile_uwsgi . --target python --tag ai/test:9004 --progress=plain
docker-compose -f deploy/docker/docker-compose-9004.yml up -d