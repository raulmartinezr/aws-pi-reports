.PHONY: docs test help
.DEFAULT_GOAL := help

SHELL := /bin/bash

export MODULE="aws_pi_reports"
export ROOTDIR:=$(shell pwd)
export CURRENT_VERSION:=$(shell poetry version -s)
export VERSION=$(shell poetry version -s)
export CURRENT_USER:=$(shell id -u ${USER}):$(shell id -g ${USER})

export PYTHON_KEYRING_BACKEND:=keyring.backends.null.Keyring

define PRINT_HELP_PYSCRIPT
import re, sys
print("You can run the following targets (with make <target>): \r\n")
for line in sys.stdin:
	match = re.match(r'^([0-9a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"


help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)



# Development


# env-create-version: export  TOX_ENV="aws_pi_reports3.8,aws_pi_reports3.9"
# env-create-version:
# 	tox -e $(TOX_ENV) --recreate

# env-create: env-create-version## (re)create a development environment using tox
# 	@echo -e "\r\nYou can activate PYTHON 3.8 environment with:\r\n\r\n$$ source ./.tox/$(TOX_ENV_38)/bin/activate\r\n"
# 	@echo -e "\r\nYou can activate PYTHON 3.9 environment with:\r\n\r\n$$ source ./.tox/$(TOX_ENV_39)/bin/activate\r\n"

# env-create-version: export  TOX_ENV="aws_pi_reports3.8,aws_pi_reports3.9"
# env-update:
# 	@[ "${TOX_ENV}" ] || ( echo "TOX_ENV is not set"; exit 1 )
# 	poetry env use $(TOX_ENV);	poetry update

env-switch-38: export PYTHON=3.8
env-switch-38: env-switch ## Switch to python 3.8 environment

env-switch-39: export PYTHON=3.9
env-switch-39: env-switch ## Switch to python 3.9 environment

env-switch-310: export PYTHON=3.10
env-switch-310: env-switch ## Switch to python 3.10 environment


env-switch: ## Switch to environment defined in PYTHON env var
	@[ "${PYTHON}" ] || ( echo "PYTHON version is not set"; exit 1 )
	poetry config virtualenvs.in-project true
	poetry env use python$(PYTHON)
	poetry install
	source .venv/bin/activate

env-update: ## Update dependencies in active environment
	poetry update

env-add-package: ## add new dependency to requirements.in
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	poetry add ${PACKAGE}

env-add-dev-package: ## add new development dependency to requirements-dev.in
	@[ "${PACKAGE}" ] || ( echo "PACKAGE is not set"; exit 1 )
	poetry add --dev ${PACKAGE}


version: ## shows the current package version
	@echo v$(CURRENT_VERSION)

poetry-version: ## bumps version and creates and commits tag
	@[ "${PART}" ] || ( echo "You must provide which PART of semantic version you want to bump: major.minor.patch"; exit 1 )
	@poetry version $(PART); \

precommit-install:
	pre-commit install

build:
	poetry build

install: ## install the package to the active Python's site-packages
	poetry install --with dev

tag-bump: poetry-version ## bumps version and creates and commits tag
	@git tag v$(VERSION)
	@echo "Please push tag to GitLab with: 'make tag-push' "


tag-push: ## Pushes tag for current version
	git push origin v$(CURRENT_VERSION)
	git push

tag-delete: ## deletes tag
	git tag -d $(TAG)
	git push --delete origin $(TAG)

.PHONY:tests
tests: ## Run tests with mocled db transport
	poetry run pytest

tests-with-db: export aws_pi_reports_MOCKED_DB=False
tests-with-db: ## Run tests with coouchdb
	poetry run pytest

lint:## Run pylint
	# poetry  run pylint --rcfile aws_pi_reports/.pylintrc -j 0 aws_pi_reports
	# poetry  run pylint --rcfile tests/.pylintrc -j 0 tests
	poetry run ruff aws_pi_reports
	poetry run ruff tests

code-check: ## Runs all pre commit code checks
	poetry run pre-commit run --all-files

code-check-diff: ## Runs all pre commit code checks with show-diff-on-failure
	poetry run pre-commit run --all-files --show-diff-on-failure

coverage:
	poetry run pytest --cov-report html:./docs/coverage/html --cov-report xml:./docs/coverage/coverage.xml --cov-report term  --cov=aws_pi_reports tests/

# Cleanup

clean-all: clean clean-envs clean-mypy-cache ## remove everything (artifacts, environments, etc.)

clean: clean-build clean-dist clean-test clean-docs ## remove all build, test, coverage and Python artifacts

clean-docs: ## remove auto-generated docs
	rm -fr docs/_build

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr .eggs/
	find $(MODULE) -name '*.c' -exec rm -f {} +

clean-dist: ## remove dist packages
	rm -fr dist/

clean-envs: ## remove virtual environments (created by tox)
	rm -fr .venv

clean-test: ## remove test and coverage artifacts
	rm -rf .pytest_cache
	rm -f .coverage

clean-mypy-cache:
	rm -rf .mypy_cache



docker-run-tests: export TARGET="tests"
docker-run-tests: docker-run ## run tests with mocked transport in docker

docker-run-tests-with-db: export TARGET="tests-with-db"
docker-run-tests-with-db: docker-start-services docker-run docker-stop-services ## run tests against counchdb in docker




docker-start-services:
	docker-compose -f docker/dev/docker-services.yml up -d
	#sleep 1

docker-stop-services:
	docker-compose -f docker/dev/docker-services.yml down

docker-run:
	docker-compose -f docker/dev/docker-compose.yml run --rm -u $(CURRENT_USER) aws_pi_reports $(MAKE) $(TARGET)

