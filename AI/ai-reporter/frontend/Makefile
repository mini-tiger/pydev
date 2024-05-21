SUFFIX ?= local
IMAGE_TAG ?= v0.8.1.4
FULL_IMAGE_TAG = $(IMAGE_TAG)-$(SUFFIX)
AI_REPORTER_IMAGE ?= ai-reporter:$(FULL_IMAGE_TAG)
CONTAINER_NAME_PROD = ai-reporter-prod-$(SUFFIX)
BUILD_TAG ?= dev

VERSION=$(shell git rev-parse --short HEAD)

build-vnet:
	$(MAKE) build-prod BUILD_TAG=vnet

build-ciecc:
	$(MAKE) build-prod BUILD_TAG=dev


build-prod:
	# Check if the image with the same version already exists
	if docker inspect ${AI_REPORTER_IMAGE} >/dev/null 2>&1; then \
		echo "Image with version ${IMAGE_TAG} already exists. Exiting..."; \
		exit 1; \
	fi
	docker build --build-arg version=$(VERSION) --build-arg build_tag=${BUILD_TAG} -t ${AI_REPORTER_IMAGE} -f docker/Dockerfile.prod .

run-prod:
	# Stop the existing container with the same name (if running)
	# docker ps -q --filter name=${CONTAINER_NAME_PROD} | xargs -r docker stop

	# Remove the existing container with the same name (if exists)
	# docker rm -f ${CONTAINER_NAME_PROD} || true

	# Run the new container
	docker run -d --name ${CONTAINER_NAME_PROD} --network host ${AI_REPORTER_IMAGE}

stop-prod:
	docker stop ${CONTAINER_NAME_PROD}

rm-prod:
	docker rm ${CONTAINER_NAME_PROD}