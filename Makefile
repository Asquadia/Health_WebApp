DOCKER_IMAGE_NAME = my-health-app
DOCKER_CONTAINER_NAME = my-health-app-container
PYTHON_INTERPRETER = ./venv/bin/python
VENV_PYTHON = /app/venv/bin/python
VENV_ACTIVATE = /app/venv/bin/activate # Full path to activate script


build:
	docker build -t $(DOCKER_IMAGE_NAME) .

run_all:
	docker run -d \
	--name $(DOCKER_CONTAINER_NAME) \
	-p 5000:5000 -p 5001:5001 -p 5002:5002 \
	$(DOCKER_IMAGE_NAME)

stop:
	docker stop $(DOCKER_CONTAINER_NAME) || true

clean: stop
	docker rm $(DOCKER_CONTAINER_NAME) || true
	docker rmi $(DOCKER_IMAGE_NAME) || true

test:
	docker exec $(DOCKER_CONTAINER_NAME) bash -c "source $(VENV_ACTIVATE) && $(VENV_PYTHON) test/test.py"

.PHONY: build run_all stop clean test
