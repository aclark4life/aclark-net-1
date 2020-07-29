include base.mk

#-------------------------------------------------------------------------------
#
# Custom Overrides
#
# https://stackoverflow.com/a/49804748

PROJECT = aclark
APP = db
.DEFAULT_GOAL=commit-push
install: pygraphviz-install pip-install
serve:
	export DEBUG=1; $(MAKE) django-serve
virtualenv: python-virtualenv-3-8
black:
	black aclark/db/*.py
	black aclark/db/management/commands/*.py
	black aclark/root/*.py
	black aclark/*.py

flake:
	-flake8 --max-line-length 100 aclark/db/*.py
	-flake8 --max-line-length 100 aclark/db/management/commands/*.py
	-flake8 --max-line-length 100 aclark/root/*.py
	-flake8 --max-line-length 100 aclark/*.py

pygraphviz-install:
	pip install --install-option="--include-path=/usr/local/include/" --install-option="--library-path=/usr/local/lib/" pygraphviz

pygraphviz-install-win:
	pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz2.38\include" --global-option="-LC:\Program Files\Graphviz2.38\lib\release\lib" pygraphviz


db-init:
	-dropdb project_app
	createdb project_app
