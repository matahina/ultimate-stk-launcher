#! /bin/sh

cd $1
svn revert --recursive .
svn up

cd $2
git reset --hard
git pull
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j10
