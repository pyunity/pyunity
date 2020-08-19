@ECHO OFF

python setup.py bdist_wheel sdist
sphinx-apidoc -F -M -o docs pyunity
git add .
git commit -m %1
git push
"docs/make" html
pip install --upgrade dist/pyunity-0.0.1-py3-none-any.whl