#!/bin/bash

DXC_PACKAGE="DirectXShaderCompiler"
DXC_VERSION="1.7.2207"

cd "$DXC_PACKAGE"
git checkout .
git apply ../build_e2k_dxc.patch

rm autoconf/config.guess
curl "http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD" --create-file-mode 755 -o autoconf/config.guess
chmod 755 autoconf/config.guess

cd external/SPIRV-Tools
git checkout .
git apply ../../../build_e2k_spriv_tools.patch
cd ../..

mkdir -p "build/"
mkdir -p "build/docs/"
cd "build/"

cmake ".." -DCMAKE_BUILD_TYPE=Release -C "../cmake/caches/PredefinedParams.cmake"
make

cd ../..
cp $DXC_PACKAGE/build/lib/libdxcompiler.so.3.7 DXC-$DXC_VERSION/lib/linux64/libdxcompiler.so
