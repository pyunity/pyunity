.PHONY: all
all: cython
		python setup.py bdist_wheel sdist

.PHONY: cython
cython:
		python prepare.py cythonize

.PHONY: test
test:
		full=1 pytest

.PHONY: docs
docs:
		python docs/build.py -x

