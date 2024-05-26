#! /bin/sh

cd $1
git clone https://github.com/kimden/stk-code.git stk-code-kimden
svn co https://svn.code.sf.net/p/supertuxkart/code/stk-assets stk-assets
cd stk-code-kimden
git checkout local-client
mkdir cmake_build
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j`if [ $(( $(nproc) - 1 )) -eq 0 ]; then echo 1; else echo $(( $(nproc) - 1 )) ; fi`
