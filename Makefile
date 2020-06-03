include base.mk

#-------------------------------------------------------------------------------
#
# Custom Overrides
#
# https://stackoverflow.com/a/49804748

PROJECT = aclark
APP = db
.DEFAULT_GOAL=commit-push
install: pip-install
serve: django-serve

black:
	black aclark/db/*.py
	black aclark/db/management/commands/*.py
	black aclark/root/*.py
	black aclark/*.py
