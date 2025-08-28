#! /bin/sh

# Thanks https://gist.github.com/kimden/178385adb5879492b68745ef9abb7f83

cd $1
git clone https://github.com/Nomagno/stk-assets.git stk-2-emt/stk-assets
git clone https://github.com/matahina/stk-code-emt-fixed.git stk-2-emt/stk-code-emt-fixed
cd stk-2-emt/stk-code-emt-fixed/
mkdir cmake_build
cd cmake_build
cmake .. -DCMAKE_BUILD_TYPE=Debug -DNO_SHADERC=ON
make -j`if [ $(( $(nproc) - 1 )) -eq 0 ]; then echo 1; else echo $(( $(nproc) - 1 )) ; fi`
