#! /bin/sh

cd $1
git clone https://github.com/supertuxkart/stk-code stk-code-speed
svn co https://svn.code.sf.net/p/supertuxkart/code/stk-assets stk-assets
cd stk-code-speed
git checkout 42d4eaa
wget https://github.com/matahina/Miscellanous-STK-files/raw/main/stk_speed_anonymouse_coder/src.zip
unzip -o src.zip
wget https://raw.githubusercontent.com/matahina/Miscellanous-STK-files/refs/heads/main/stk_speed_anonymouse_coder/0001-patcherella.patch
git apply 0001-patcherella.patch
mkdir cmake_build
cd cmake_build
cmake ..
make -j`if [ $(( $(nproc) - 1 )) -eq 0 ]; then echo 1; else echo $(( $(nproc) - 1 )) ; fi`
