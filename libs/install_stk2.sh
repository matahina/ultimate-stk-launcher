#! /bin/sh

cd $1
git clone https://github.com/Alayan-stk-2/stk-code.git alayan/stk-code-alayan
cd alayan
svn co https://svn.code.sf.net/p/supertuxkart/code/stk-assets stk-assets
cd stk-assets
wget -O assets.zip "https://mascots.moe/stk/test2x/stk-assets-change.zip"
unzip assets.zip
yes | cp -rf stk-assets-change/models/* models/
yes | cp -rf stk-assets-change/sfx/* sfx/
yes | cp -rf stk-assets-change/textures/* textures/
rm -R stk-assets-change
cd ../stk-code-alayan
git checkout BalanceSTK2
mkdir cmake_build
cd cmake_build
cmake ..
make -j10
