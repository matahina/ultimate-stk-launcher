#! /bin/sh

# Thanks https://gist.github.com/kimden/178385adb5879492b68745ef9abb7f83

cd $1
mkdir stk-2-emt
cd stk-2-emt
git clone https://github.com/matahina/stk-code-emt-fixed.git
cd stk-code-emt-fixed
git remote add upstream https://github.com/Nomagno/stk-code.git
git fetch upstream --tags
# Get latest tag name
latestTag=$(git describe --tags "$(git rev-list --tags --max-count=1)")
cd ../
wget https://github.com/Nomagno/stk-code/releases/download/$latestTag/stk-assets.zip
unzip stk-assets.zip
rm stk-assets.zip
cd stk-code-emt-fixed/
mkdir cmake_build
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=Debug -DNO_SHADERC=ON
make -j`if [ $(( $(nproc) - 1 )) -eq 0 ]; then echo 1; else echo $(( $(nproc) - 1 )) ; fi`
