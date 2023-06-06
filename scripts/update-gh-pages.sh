#!/bin/bash

# this script is used in .github/workflows/build.yml
# it assumes the main branch is in folder "main"
# the gh-pages branch is in folder "gp-pages"

cp -rf ./main/doc/build/html/* ./pg-pages/

cd ./pg-pages/

git add -A
git commit --message "GitHub Action to update github pages"
git push origin