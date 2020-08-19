python setup.py bdist_wheel sdist
pip install --upgrade dist/pyunity-0.0.1-py3-none-any.whl
python -m pyunity
git add .
git commit -m $1
git push