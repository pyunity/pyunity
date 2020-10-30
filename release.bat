@ECHO OFF
git checkout master
twine upload --repository testpypi dist/0.2.0/pyunity-0.2.0*
twine upload dist/0.2.0/pyunity-0.2.0*
git checkout releases
twine upload --repository testpypi 0.2.0/pyunity-0.2.0*
twine upload 0.2.0/pyunity-0.2.0*
git checkout master