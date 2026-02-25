#!/bin/zsh

DXC_PACKAGE="DirectXShaderCompiler"
DXC_VERSION="1.8.2505.1"

mkdir -p build
mkdir -p build/docs
cd build

cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64" -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_CXX_FLAGS=-Werror -DCMAKE_CXX_FLAGS=-Wno-deprecated-declarations -C ../$DXC_PACKAGE/cmake/caches/PredefinedParams.cmake ../$DXC_PACKAGE
cmake --build .

cd ..
cp build/lib/libdxcompiler.dylib DXC-$DXC_VERSION/lib/macosx/dxcompiler.dylib
