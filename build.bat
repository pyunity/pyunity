@ECHO OFF

del /s *.pyd
python setup.py bdist_wheel sdist
RMDIR /S /Q "build/" /S /Q "pyunity.egg-info/" /S /Q "docs/build/html/"
sphinx-build -T -E -b html docs/source docs/build/html
IF NOT [%1] == [] (
git add .
git commit -m %1
git push
)