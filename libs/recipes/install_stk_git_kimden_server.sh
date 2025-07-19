#! /bin/sh

cd $1
git clone https://github.com/kimden/stk-code.git stk-code-kimden-server
svn co https://svn.code.sf.net/p/supertuxkart/code/stk-assets stk-assets
cd stk-code-kimden-server
mkdir cmake_build
cd cmake_build
cmake .. -DSERVER_ONLY=ON -DUSE_SQLITE3=ON -DWEB_SUPPORT=ON -DUSE_RECORDS_V2=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j`if [ $(( $(nproc) - 1 )) -eq 0 ]; then echo 1; else echo $(( $(nproc) - 1 )) ; fi`
