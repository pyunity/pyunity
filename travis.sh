yset a=1
python prepare.py -x || python3 prepare.py -x
python setup.py bdist_wheel -d .. || python3 setup.py bdist_wheel -d ..
git checkout .
git checkout -b releases --track origin/releases
git clean -d -f -f
mv ../pyunity*.whl 0.2.0/
git remote set-url origin https://rayzchen:${GH_TOKEN}@github.com/rayzchen/pyunity.git
git config --global user.name "rayzchen"
git config --global user.email "tankimarshal2@gmail.com"
git config pull.rebase true
git add .
git commit -m "Travis build $TRAVIS_BUILD_NUMBER [ci skip]"
git pull
while ! git push --set-upstream origin releases; do
    sleep 1 # or more, or less
done