#! /bin/sh

cd $1
svn revert --recursive .
svn up

cd $2
git reset --hard
git pull
cd cmake_build
cmake .. -DSERVER_ONLY=ON -DUSE_SQLITE3=ON -DWEB_SUPPORT=ON -DUSE_RECORDS_V2=ON -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j$(( $(nproc) - 1 ))

# Optional, if you have specific commands to add, create that file
test -f ../../server_hooks.sh && sh ../../server_hooks.sh
