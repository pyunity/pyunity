python setup.py bdist_wheel sdist
cd dist
pip install --upgrade pyunity-0.0.1-py3-none-any.whl
cd ../tests
python test1.py
cd ..