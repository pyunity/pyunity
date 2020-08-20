@ECHO OFF

python setup.py bdist_wheel sdist
RMDIR /S /Q build /S /Q pyunity.egg-info /S /Q docs/build/html
REM pip install --upgrade dist/pyunity-0.0.1-py3-none-any.whl
sphinx-apidoc -F -M -o docs/source pyunity
sphinx-build -b html docs/source docs/build/html
git add .
git commit -m %1
git push