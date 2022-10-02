SHELL := /bin/bash
CWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

IMG = capstone
BASE_IMG = capstone-base
TEST_IMG = capstone-test
IMG_TAG ?= latest
NOTEBOOK_TAG ?= notebook

PORT ?= 8080
JUPYTER_PORT ?= 8888

LOCAL_DATA_DIR = ${CWD}data
LOCAL_MODEL_DIR = ${CWD}model
LOCAL_REPORTS_DIR = ${CWD}reports
LOCAL_NOTEBOOKS_DIR = ${CWD}notebooks

DOCKER_DATA_DIR = /usr/src/app/data
DOCKER_MODEL_DIR = /usr/src/app/model
DOCKER_REPORTS_DIR = /usr/src/app/reports
DOCKER_NOTEBOOKS_DIR = /usr/src/app/notebooks

export

.PHONY: check-env
check-env:
ifndef AWS_ACCESS_KEY_ID
	$(error AWS_ACCESS_KEY_ID is undefined)
endif
ifndef AWS_SECRET_ACCESS_KEY
	$(error AWS_SECRET_ACCESS_KEY is undefined)
endif
ifndef AWS_DEFAULT_REGION
	$(error AWS_DEFAULT_REGION is undefined)
endif
ifndef OPENAI_API_KEY_BETA
	$(error OPENAI_API_KEY_BETA is undefined)
endif
ifndef OPENAI_API_KEY
	$(error OPENAI_API_KEY is undefined)
endif

.PHONY: build-base
build-base: check-env
	@docker build \
		-t ${BASE_IMG}:${IMG_TAG} \
		-f Dockerfile.base \
		.

.PHONY: build
build: build-base
	docker build \
		-t ${IMG}:${IMG_TAG} \
		--build-arg IMAGE=${BASE_IMG}:${IMG_TAG} .

.PHONY: test-image
test-image: build-base
	docker build \
		-t ${TEST_IMG}:${IMG_TAG} \
		-f Dockerfile.test \
		--build-arg IMAGE=${BASE_IMG}:${IMG_TAG} .

.PHONY: build-notebook
build-notebook: build-base
	docker build \
		-t ${IMG}:${NOTEBOOK_TAG} \
		--build-arg IMAGE=${BASE_IMG}:${IMG_TAG} \
		--build-arg JUPYTER_PORT=${JUPYTER_PORT} \
		-f Dockerfile.jupyter .

.PHONY: notebook
notebook: build-notebook
	docker run -it --rm \
		--volume ${LOCAL_DATA_DIR}:${DOCKER_DATA_DIR} \
		--volume ${LOCAL_NOTEBOOKS_DIR}:${DOCKER_NOTEBOOKS_DIR} \
		--env "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" \
		--env "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" \
		--env "AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}" \
		--env "OPENAI_API_KEY_BETA=${OPENAI_API_KEY_BETA}" \
		--env "OPENAI_API_KEY=${OPENAI_API_KEY}" \
		--publish ${JUPYTER_PORT}:${JUPYTER_PORT} \
		${IMG}:${NOTEBOOK_TAG} jupyter notebook \
		--port=${JUPYTER_PORT} \
		--allow-root \
		--ip=0.0.0.0

test: test-image
	docker run -t ${TEST_IMG}:${IMG_TAG}

fetch:
	docker run -t \
		--volume ${LOCAL_DATA_DIR}:${DOCKER_DATA_DIR} \
		--env "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}" \
		--env "AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}" \
		--env "AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION}" \
		${IMG}:${IMG_TAG} fetch
