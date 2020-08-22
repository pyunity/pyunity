python setup.py bdist_wheel sdist
rm -rf build/ pyunity.egg-info/ docs/build/html/
find docs/source/* ! -name conf.py -delete
sphinx-apidoc -e F -M -o docs/source pyunity pyunity/config.py
sphinx-build -b html docs/source docs/build/html
git clean -d -f -f
git add .
git commit -m $1
git push
pip install --upgrade dist/pyunity-0.0.3-py3-none-any.whl