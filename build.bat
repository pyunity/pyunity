@ECHO OFF

python setup.py bdist_wheel sdist
RMDIR /S /Q "build/" /S /Q "pyunity.egg-info/" /S /Q "docs/build/html/"
sphinx-apidoc -e -F -M -o docs/source pyunity pyunity/config.py pyunity/examples/*
sphinx-build -T -E -b html docs/source docs/build/html
git add .
git commit -m %1
git push
pip install --upgrade dist/pyunity-0.0.4-py3-none-any.whl