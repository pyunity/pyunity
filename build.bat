@ECHO OFF

python setup.py bdist_wheel sdist
pip install --upgrade dist/pyunity-0.0.1-py3-none-any.whl
sphinx-apidoc -F -M -o docs pyunity
sphinx-build -b html docs docs/_build/_html
git add .
git commit -m %1
git push