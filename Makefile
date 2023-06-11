.PHONY: all
all: cython
		python -m build

.PHONY: cython
cython:
		python prepare.py cythonize

.PHONY: test
test:
		full=1 pytest

.PHONY: docs
docs:
		python docs/build.py -x

