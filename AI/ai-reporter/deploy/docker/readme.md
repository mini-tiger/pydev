
DOCKER_BUILDKIT=1 docker build -f deploy/docker/Dockerfile_uwsgi . --target python --tag ai/test:nginx --progress=plain
docker-compose -f deploy/docker/docker-compose.yml up -d
