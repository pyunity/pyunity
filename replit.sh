pip install cython
python setup.py bdist_wheel -d ..
git checkout HEAD .
mv ../pyunity-0.2.0-cp38-cp38-linux_x86_64.whl dist/0.2.0/