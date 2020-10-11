pip install cython
python prepare.py
python setup.py bdist_wheel -d ..
rm -rf build/ pyunity.egg-info/
mv ../pyunity-0.2.0-cp38-cp38-linux_x86_64.whl dist/0.2.0/