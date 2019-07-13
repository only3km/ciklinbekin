#!/bin/sh
setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI (on behalf of @ztl8702)"
}

commit_website_files() {
  cp -rf ./build /tmp/
  git checkout -b gh-pages-test
  rm -rf ./
  cp -rf /tmp/build/**/* ./
  git add .
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

upload_files() {
  git remote add origin-pages https://${GH_TOKEN}@github.com/only3km/ciklinbekin.git > /dev/null 2>&1
  git push --quiet --set-upstream origin-pages gh-pages-test
}

setup_git
commit_website_files
upload_files
