@ECHO OFF

py -m unittest tests.py
py -m autopep8 -i -r --ignore E301,E302 pyunity setup.py prepare.py cli.py
py prepare.py
py -3.6 setup.py build -c mingw32 bdist_wheel -d dist\0.3.1\
py -3.7 setup.py build -c mingw32 bdist_wheel -d dist\0.3.1\
py -3.8 setup.py build -c mingw32 bdist_wheel -d dist\0.3.1\
py setup.py build -c mingw32 bdist_wheel -d dist\0.3.1\ sdist -d dist\0.3.1\
RMDIR /S /Q src\ docs\en\
DEL docs\source\pyunity*
sphinx-apidoc -e -F -M -o docs\source pyunity pyunity\config.py pyunity\examples\*
sphinx-build -T -E -b html docs\source docs\en
RMDIR /S /Q build\ pyunity.egg-info\ 
IF NOT [%1] == [] (
git add .
git commit -m %1
git push
)
start py -3.6 -m pip install -U dist\0.3.1\pyunity-0.3.1-cp36-cp36m-win32.whl
start py -3.7 -m pip install -U dist\0.3.1\pyunity-0.3.1-cp37-cp37m-win32.whl
start py -3.8 -m pip install -U dist\0.3.1\pyunity-0.3.1-cp38-cp38-win32.whl
py -m pip install -U dist\0.3.1\pyunity-0.3.1-cp39-cp39-win32.whl