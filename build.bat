@ECHO OFF

python setup.py bdist_wheel sdist
RMDIR /S /Q "build/" /S /Q "pyunity.egg-info/" /S /Q "docs/build/html/"
sphinx-apidoc -F -M -o docs/source pyunity pyunity/config.py
sphinx-build -b html docs/source docs/build/html
git add .
git commit -m %1
git push
pip install --upgrade dist/pyunity-0.0.1-py3-none-any.whl