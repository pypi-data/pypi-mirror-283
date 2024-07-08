.PHONY: help venv remove-venv develop develop-conda dist testpypi-upload pypi-upload clean test
SHELL := /bin/bash

# keep all in current directory, not spread in conda system/user folders:
# <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#specifying-a-location-for-an-environment>
VENV_NAME  ?= venv
VENV_BIN   := $(shell pwd)/${VENV_NAME}/bin
VENV_OK    := $(VENV_BIN)/activate

CONDA_BASE := $(shell conda info --base)
CONDA_INIT       = source "$(CONDA_BASE)/etc/profile.d/conda.sh"
CONDA_ACTIVATE   = conda activate $(VENV_NAME)/
CONDA_DEACTIVATE = conda deactivate

PKG_NAME := climdex-kit # FIXME duplicate in setup.py
PYTHON := ${VENV_BIN}/python3

.DEFAULT: help
help:
	@echo "make venv"
	@echo "       create the virtual environment with all deps"
	@echo "make develop"
	@echo "       install the package in the venv with pip in development ``editable'' mode"
	@echo "make dist"
	@echo "       build the sdist and wheel distribution files under dist/ (version inferred from scm)"
	@echo "make testpypi-upload"
	@echo "       uploads the distribution files to the TestPyPI server"
	@echo "make pypi-upload"
	@echo "       uploads the distribution files to the official PyPI server"
	@echo "make test"
	@echo "       run tests"
	@echo "make clean"
	@echo "       removes temporary files"

venv: $(VENV_OK)

.ONESHELL:
$(VENV_OK): setup.py environment.yml
	if [ -d $(VENV_BIN) ]
	then
	    conda env update --prefix $(VENV_NAME) --file environment.yml  --prune
	else
	    conda env create --prefix $(VENV_NAME) --file environment.yml
	    conda config --set env_prompt '({name})'
	fi
	touch $(VENV_OK)
	# --> conda activate venv/

remove-venv:
	$(CONDA_INIT)
	$(CONDA_DEACTIVATE)
	conda env remove --prefix $(VENV_NAME)

develop: venv
	$(CONDA_INIT)
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pip install -e .

develop-conda: venv
	@echo "conda development installation not recommended yet. Please run `make develop-pip`"
	@echo "See https://github.com/conda/conda-build/issues/1992"
	$(CONDA_INIT)
	$(CONDA_ACTIVATE)
	#conda build -V &>/dev/null || conda install conda-build
	#conda develop .

uninstall: venv
	$(CONDA_INIT)
	$(CONDA_ACTIVATE)
	$(PYTHON) -m pip uninstall $(PKG_NAME)

dist: venv
	$(PYTHON) -m build
	
testpypi-upload: venv
	$(PYTHON) -m twine upload --repository testpypi dist/*

pypi-upload: venv
	$(PYTHON) -m twine upload dist/*

clean:
	find . -name '*.pyc' -exec rm -fv {} +
	rm -rfv *.eggs *.egg-info dist/ build/ docs/_build .cache

test:
	$(PYTHON) -m unittest discover tests/

