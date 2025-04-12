#! /bin/sh

cd $1
git reset --hard
git pull
# Get new tags from remote
git fetch --tags
# Get latest tag name
latestTag=$(git describe --tags "$(git rev-list --tags --max-count=1)")
cd ../
rm -R stk-assets
wget https://github.com/Nomagno/stk-code/releases/download/$latestTag/stk-assets.zip
unzip stk-assets.zip
rm stk-assets.zip
cd stk-code/
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=Debug -DNO_SHADERC=ON
make -j`if [ $(( $(nproc) - 1 )) -eq 0 ]; then echo 1; else echo $(( $(nproc) - 1 )) ; fi`
