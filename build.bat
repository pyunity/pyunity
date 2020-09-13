@ECHO OFF

IF NOT [%1] == [-x] (
SET CYTHON=1
DEL /s *.pyd
DEL /s *.so
SET MSG=%2
) ELSE SET MSG=%1
python setup.py bdist_wheel sdist
IF [%1] == [-x] SET CYTHON=
RMDIR /S /Q "build/" /S /Q "pyunity.egg-info/" /S /Q "docs/build/html/"
sphinx-build -T -E -b html docs/source docs/build/html
IF NOT [%MSG%] == [] (
git add .
git commit -m %MSG%
git push
)
set MSG=