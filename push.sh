#!/bin/sh
setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI (on behalf of @ztl8702)"
}

prepare() {
  cp -rf ./build /tmp/
}

checkout() {
  git remote update
  git fetch 
  git checkout --track origin/gh-pages
  git checkout -b gh-pages-new
}

checkout_pr() {
  git checkout gh-pages
  git pull
  git checkout -b gh-pages-review
}

commit_website_files() {
  git rm -r '*'
  rm -rf ./*
  cp -rf /tmp/build/* ./
  git add .
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER"
}

auth() {
  git remote add origin-ci https://${GH_TOKEN}@github.com/only3km/ciklinbekin.git > /dev/null 2>&1
}

upload_files() {
  git checkout gh-pages
  git reset --hard gh-pages-new --
  git push --quiet --set-upstream origin-ci --force gh-pages
}

upload_files_pr() {
  git push --quiet --set-upstream origin-ci --force gh-pages-review
}

setup_git
auth
prepare
if [ "$TRAVIS_BRANCH" = "master" ] && [ "$TRAVIS_PULL_REQUEST" = "false" ]; then
  checkout
else
  checkout_pr
fi
commit_website_files
if [ "$TRAVIS_BRANCH" = "master" ] && [ "$TRAVIS_PULL_REQUEST" = "false" ]; then
  upload_files
else
  if [ "$TRAVIS_SECURE_ENV_VARS" = "true" ]; then
    upload_files_pr
  fi
fi
