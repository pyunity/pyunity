python setup.py bdist_wheel sdist
pip install --upgrade dist/pyunity-0.0.1-py3-none-any.whl
git add .
git commit -m %1
git push
python -m pyunity