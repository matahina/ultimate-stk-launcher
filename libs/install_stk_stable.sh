#! /bin/sh

cd $1
git clone https://github.com/supertuxkart/stk-code stk-code-stable
svn co https://svn.code.sf.net/p/supertuxkart/code/stk-assets stk-assets
cd stk-code-stable
git checkout 1.4-branch
mkdir cmake_build
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j10
