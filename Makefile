PROJECT = schedulark
COVFILE ?= .coverage
PART ?= patch


clean:
		find . -name '__pycache__' -exec rm -fr {} +
		find . -name '.pytest_cache' -exec rm -fr {} +
		find . -name '.mypy_cache' -exec rm -fr {} +
		find . -name 'pip-wheel-metadata' -exec rm -fr {} +
		find . -name '$(PROJECT).egg-info' -exec rm -fr {} +

test:
		pytest

mypy:
		mypy $(PROJECT)

push:
		git push && git push --tags


coverage:
		export COVERAGE_FILE=$(COVFILE); pytest -x --cov-branch \
		--cov=$(PROJECT) tests/ --cov-report term-missing -s -o \
		cache_dir=/tmp/.pytest_cache -vv


version:
		bump2version $(PART) pyproject.toml $(PROJECT)/__init__.py --tag --commit

gitmessage:
		touch .gitmessage
		echo "\n# commit message\n.gitmessage" >> .gitignore
		git config commit.template .gitmessage
