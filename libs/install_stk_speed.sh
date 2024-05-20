#! /bin/sh

cd $1
git clone https://github.com/supertuxkart/stk-code stk-code-speed
svn co https://svn.code.sf.net/p/supertuxkart/code/stk-assets stk-assets
cd stk-code-speed
git checkout 42d4eaa
wget https://github.com/matahina/Miscellanous-STK-files/raw/main/stk_speed_anonymouse_coder/src.zip
unzip -o src.zip
mkdir cmake_build
cd cmake_build
cmake ..
make -j10
