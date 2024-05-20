#! /bin/sh

cd $1
svn revert --recursive .
svn up
wget -O assets.zip "https://mascots.moe/stk/test2x/stk-assets-change.zip"
unzip assets.zip
yes | cp -rf stk-assets-change/models/* models/
yes | cp -rf stk-assets-change/sfx/* sfx/
yes | cp -rf stk-assets-change/textures/* textures/
rm -R stk-assets-change

cd $2
git reset --hard
git pull
cd cmake_build
cmake ..
make -j10
