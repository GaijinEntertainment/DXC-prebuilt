#!/bin/bash

DXC_PACKAGE="DirectXShaderCompiler"
DXC_VERSION="1.8.2407"

cd "$DXC_PACKAGE"

mkdir -p "build/"
cd "build/"

cmake ".." -GNinja -DCMAKE_BUILD_TYPE=Release -C "../cmake/caches/PredefinedParams.cmake"
ninja

cd ../..
cp $DXC_PACKAGE/build/lib/libdxcompiler.so DXC-$DXC_VERSION/lib/linux64/libdxcompiler.so
