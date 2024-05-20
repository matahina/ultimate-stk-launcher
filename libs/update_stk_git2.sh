#! /bin/sh

cd $1
git reset --hard
git pull

cd $2
git reset --hard
git pull
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=Debug -DNO_SHADERC=ON
make -j10
