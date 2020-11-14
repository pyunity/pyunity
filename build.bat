@ECHO OFF

tests.py
py -m autopep8 -i -r --ignore E301,E302 pyunity setup.py cli.py
prepare.py
setup.py build -c mingw32 bdist_wheel -d "dist/0.3.0/" sdist -d "dist/0.3.0/"
py -3.7 setup.py build -c mingw32 bdist_wheel -d "dist/0.3.0/"
py -3.6 setup.py build -c mingw32 bdist_wheel -d "dist/0.3.0/"
RMDIR /S /Q "pyunity.egg-info/" "build/" "docs/en/"
DEL "docs/source/pyunity*"
sphinx-apidoc -e -F -M -o docs/source pyunity pyunity/config.py pyunity/examples/*
sphinx-build -T -E -b html docs/source docs/en
IF NOT [%1] == [] (
git add .
git commit -m %1
git push
)
pip install -U "dist/0.3.0/pyunity-0.3.0-cp38-cp38-win32.whl"
py -3.7 -m pip install -U "dist/0.3.0/pyunity-0.3.0-cp37-cp37m-win32.whl"
py -3.6 -m pip install -U "dist/0.3.0/pyunity-0.3.0-cp36-cp36m-win32.whl"