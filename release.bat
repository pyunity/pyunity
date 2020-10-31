@ECHO OFF
git checkout master
twine upload --repository testpypi dist/0.2.1/pyunity-0.2.1*
twine upload dist/0.2.1/pyunity-0.2.1*
git checkout releases
twine upload --repository testpypi 0.2.1/pyunity-0.2.1*
twine upload 0.2.1/pyunity-0.2.1*
git checkout master