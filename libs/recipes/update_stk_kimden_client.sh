#! /bin/sh

cd $1
svn revert --recursive .
svn up

cd $2
git reset --hard
git pull
wget https://raw.githubusercontent.com/matahina/Miscellanous-STK-files/refs/heads/main/patch_the_kimden_local_client/0001-the_commit.patch
git apply 0001-the_commit.patch
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j`if [ $(( $(nproc) - 1 )) -eq 0 ]; then echo 1; else echo $(( $(nproc) - 1 )) ; fi`
