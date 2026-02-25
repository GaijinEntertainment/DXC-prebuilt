#!/bin/bash

DXC_PACKAGE="DirectXShaderCompiler"
DXC_VERSION="1.8.2505.1"

cd "$DXC_PACKAGE"
git checkout .
git apply ../build_e2k_dxc.patch

rm autoconf/config.guess
wget -O autoconf/config.guess 'https://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod 755 autoconf/config.guess

cd external/SPIRV-Tools
git checkout .
git apply ../../../build_e2k_spriv_tools.patch
cd ../..

mkdir -p "build/"
mkdir -p "build/docs/"
cd "build/"

cmake ".." -DCMAKE_BUILD_TYPE=Release -C "../cmake/caches/PredefinedParams.cmake"
make -j$(nproc)

cd ../..
cp $DXC_PACKAGE/build/lib/libdxcompiler.so DXC-$DXC_VERSION/lib/linux64/libdxcompiler.so
