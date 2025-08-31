## Build requirements

Requirements for building DXC package:
* Install Python 3
* Install cmake and ninja (`sudo apt install cmake` and `sudo apt install ninja-build` for Ubuntu)

## How to Build

First start `python3 s1_prepare_package.py`, this will clone [DXC repo from github](https://github.com/microsoft/DirectXShaderCompiler), checkout required version and download prebuilt win64 package.
Then it will create base DXC-x.x.xxxx folder composed of actual include and lib folders (with `lib/win64` being filled with content of prebuilt win64 package)

Next start `s2_build_linux64.sh` (on linux) or `s2_build_macosx.sh` (on macOS) to build libdxcompiler.so and dxcompiler.dylib respectively.

The last step (optional) is to run `s3_make_package.sh` which will build `.tar.gz` for DXC-x.x.xxxx folder (you should copy built libs from foreign OS first).

## Releases

Releases will contain packaged `.tar.gz` archive with includes and prebuilt dynamic libs for win64, linux and macOS.

Currently used DXC version is: 1.8.2407
