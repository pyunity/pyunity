@ECHO OFF

python setup.py bdist_wheel sdist
RMDIR /S /Q build /S /Q pyunity.egg-info
pip install --upgrade dist/pyunity-0.0.1-py3-none-any.whl
sphinx-apidoc -F -M -o docs pyunity config.py
sphinx-build -b html docs docs/_build/_html
git add .
git commit -m %1
git push