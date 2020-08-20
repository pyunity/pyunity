@ECHO OFF

python setup.py bdist_wheel sdist
sphinx-apidoc -F -M -o docs pyunity
sphinx-build -b html docs docs/_build/_html
if %1 == "-c" (
git add .
git commit -m %2
git push
)
pip install --upgrade dist/pyunity-0.0.1-py3-none-any.whl