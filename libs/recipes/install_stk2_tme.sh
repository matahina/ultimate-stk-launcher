#! /bin/sh

# Thanks https://gist.github.com/kimden/178385adb5879492b68745ef9abb7f83

cd $1
mkdir stk-2-tme
cd stk-2-tme
git clone https://github.com/Nomagno/stk-code.git
cd stk-code
# Get new tags from remote
git fetch --tags
# Get latest tag name
latestTag=$(git describe --tags "$(git rev-list --tags --max-count=1)")
cd ../
wget https://github.com/Nomagno/stk-code/releases/download/$latestTag/stk-assets.zip
unzip stk-assets.zip
rm stk-assets.zip
cd stk-code/
mkdir cmake_build
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=Debug -DNO_SHADERC=ON
make -j`if [ $(( $(nproc) - 1 )) -eq 0 ]; then echo 1; else echo $(( $(nproc) - 1 )) ; fi`
