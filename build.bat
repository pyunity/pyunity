@ECHO OFF

python setup.py build -c mingw32 bdist_wheel -d "dist/0.0.6/" sdist -d "dist/0.0.6/"
RMDIR /S /Q "build/" "pyunity.egg-info/" "docs/build/html/"
sphinx-build -T -E -b html docs/source docs/build/html
IF NOT [%1] == [] (
git add .
git commit -m %1
git push
)