#! /bin/sh

# Thanks https://gist.github.com/kimden/178385adb5879492b68745ef9abb7f83

cd $1
git clone https://github.com/Pttn/stk-assets.git stk-2/stk-assets
git clone https://github.com/Alayan-stk-2/stk-code.git stk-2/stk-code-alayan
cd stk-2/stk-code-alayan
git checkout BalanceSTK2
mkdir cmake_build
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=Debug -DNO_SHADERC=ON
make -j`if [ $(( $(nproc) - 1 )) -eq 0 ]; then echo 1; else echo $(( $(nproc) - 1 )) ; fi`
