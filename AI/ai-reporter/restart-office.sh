#!/bin/bash

docker stop ai-frontend-office && docker rm ai-frontend-office
docker-compose  -f deploy/docker/docker-compose-office.yml up -d
