#!/usr/bin/env bash
cd /github/workspace/
NAME=cp$(echo $1 | cut --complement -b 2)
PYTHON=$(ls /opt/python/$NAME-$NAME*/bin/python)
$PYTHON -m pip install "cython>=3.0.0a8" wheel
$PYTHON setup.py egg_info
test -f pyunity.egg-info/version.json || exit 1
$PYTHON setup.py bdist_wheel -d tmp
auditwheel repair -w dist tmp/*
