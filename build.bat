@ECHO OFF

python prepare.py
python setup.py build -c mingw32 bdist_wheel -d "dist/0.2.0/" sdist -d "dist/0.2.0/"
RMDIR /S /Q "pyunity.egg-info/" "docs/build/html/"
py -3.7 setup.py build -c mingw32 bdist_wheel -d "dist/0.2.0/"
RMDIR /S /Q "pyunity.egg-info/" "build/"
sphinx-build -T -E -b html docs/source docs/build/html
IF NOT [%1] == [] (
git add .
git commit -m %1
git push
)
py -m pip install "dist/0.2.0/pyunity-0.2.0-cp38-cp38-win32.whl" --upgrade
py -3.7 -m pip install "dist/0.2.0/pyunity-0.2.0-cp37-cp37m-win32.whl" --upgrade