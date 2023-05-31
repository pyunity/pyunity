#!/usr/bin/env bash
NAME=cp$(echo $1 | cut --complement -b 2)
PYTHON=$(ls /opt/python/$NAME-$NAME*/bin/python)
$PYTHON -m pip install -r .github/build_requirements.txt
$PYTHON setup.py egg_info
test -f pyunity.egg-info/version.json || exit 1
$PYTHON -m build -w -o tmp
auditwheel repair -w dist tmp/*
