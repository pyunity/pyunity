@ECHO OFF

prepare.py
setup.py build -c mingw32 bdist_wheel -d "dist/0.3.0/" sdist -d "dist/0.3.0/"
py -3.7 setup.py build -c mingw32 bdist_wheel -d "dist/0.3.0/"
py -3.6 setup.py build -c mingw32 bdist_wheel -d "dist/0.3.0/"
RMDIR /S /Q "pyunity.egg-info/" "build/" "docs/en/"
sphinx-build -T -E -b html docs/source docs/en
IF NOT [%1] == [] (
git add .
git commit -m %1
git push
)
pip install "dist/0.3.0/pyunity-0.3.0-cp38-cp38-win32.whl" --upgrade
py -3.7 -m pip install "dist/0.3.0/pyunity-0.3.0-cp37-cp37m-win32.whl" --upgrade
py -3.6 -m pip install "dist/0.3.0/pyunity-0.3.0-cp36-cp36m-win32.whl" --upgrade