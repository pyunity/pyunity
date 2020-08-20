python setup.py bdist_wheel sdist
rm -rf build/ pyunity.egg-info/ docs/build/html/
sphinx-apidoc -F -M -o docs/source pyunity pyunity/config.py
sphinx-build -b html docs/source docs/build/html
git add .
git commit -m $1
git push
pip install --upgrade dist/pyunity-0.0.1-py3-none-any.whl