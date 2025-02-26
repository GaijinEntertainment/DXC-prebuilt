#!/bin/bash
# sometimes this script should be run under devtoolset prefix (e.g. for CentOS 7):
# scl enable devtoolset-11 llvm-toolset-7.0 './s2_build_linux64_cmake3.sh'

DXC_PACKAGE="DirectXShaderCompiler"
DXC_VERSION="1.8.2407"

cd "$DXC_PACKAGE"

mkdir -p "build/"
mkdir -p "build/docs/"
cd "build/"

cmake3 ".." -G"Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -C../cmake/caches/PredefinedParams.cmake
cmake3 --build .

cd ../..
cp $DXC_PACKAGE/build/lib/libdxcompiler.so.3.7 DXC-$DXC_VERSION/lib/linux64/libdxcompiler.so
