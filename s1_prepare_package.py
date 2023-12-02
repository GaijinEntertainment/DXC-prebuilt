#!/usr/bin/python3
import sys
if sys.version_info.major < 3:
  print("\nERROR: Python 3 or a higher version is required to run this script.")
  exit(1)

import subprocess
import pathlib
import os
import urllib
import ssl
import ctypes
import zipfile
import shutil
from urllib import request

ssl._create_default_https_context = ssl._create_unverified_context

def run(cmd):
  try:
    print('Running: {0}'.format(cmd))
    subprocess.run(cmd, shell = True, check = True)
  except subprocess.CalledProcessError as e:
    error('subprocess.run failed with a non-zero exit code. Error: {0}'.format(e))
  except OSError as e:
    print('An OSError occurred, subprocess.run command may have failed. Error: {0}'.format(e))

def download_url2(url, file):
  file = ".packages/{0}".format(file)
  if not pathlib.Path(file).exists():
    print("Downloading '{0}' to '{1}' ...".format(url, file));
    response = request.urlretrieve(url, file)
  else:
    print("Package '{0}' already exists".format(file));

def download_url(url):
  path, file = os.path.split(os.path.normpath(url))
  download_url2(url, file)

def clone_git_repo(DXC_PACKAGE, DXC_VERSION):
  prev_cwd = os.getcwd()
  if not pathlib.Path(DXC_PACKAGE).exists():
    run('git clone "https://github.com/microsoft/{0}.git"'.format(DXC_PACKAGE))

  os.chdir(os.path.normpath(DXC_PACKAGE))
  run('git fetch --all --tags')
  run('git reset --hard origin/main')
  run('git checkout v{0}'.format(DXC_VERSION))
  if DXC_VERSION == '1.7.2207':
    run('git cherry-pick 47f31378a9b51894b0465b33ac1d10ce6349a468')
    run('git cherry-pick 396e45cbc49cfba17adf3e813064b07ab4373659')
  run({'git submodule init'})
  run({'git submodule update'})
  os.chdir(prev_cwd)

def download_prebuilt_win(DXC_PACKAGE, DXC_VERSION, DXC_BIN_ZIP):
  download_url('https://github.com/microsoft/{0}/releases/download/v{1}/{2}'.format(DXC_PACKAGE, DXC_VERSION, DXC_BIN_ZIP))
  with zipfile.ZipFile(os.path.normpath('.packages/{0}'.format(DXC_BIN_ZIP)), 'r') as zip_file:
    zip_file.extractall('.packages/_win')

# prepare base package data
DXC_PACKAGE = 'DirectXShaderCompiler'
DXC_VERSION = '1.7.2207'
DXC_BIN_ZIP = 'dxc_2022_07_18.zip'

pathlib.Path('.packages').mkdir(parents=True, exist_ok=True)
clone_git_repo(DXC_PACKAGE, DXC_VERSION)
download_prebuilt_win(DXC_PACKAGE, DXC_VERSION, DXC_BIN_ZIP)

if pathlib.Path('DXC-{0}'.format(DXC_VERSION)).exists():
  shutil.rmtree('DXC-{0}'.format(DXC_VERSION))
pathlib.Path('DXC-{0}/include'.format(DXC_VERSION)).mkdir(parents=True, exist_ok=True)
pathlib.Path('DXC-{0}/lib'.format(DXC_VERSION)).mkdir(parents=True, exist_ok=True)
pathlib.Path('DXC-{0}/lib/win64'.format(DXC_VERSION)).mkdir(parents=True, exist_ok=True)
pathlib.Path('DXC-{0}/lib/linux64'.format(DXC_VERSION)).mkdir(parents=True, exist_ok=True)
pathlib.Path('DXC-{0}/lib/macosx'.format(DXC_VERSION)).mkdir(parents=True, exist_ok=True)

shutil.copy2('{0}/LICENSE.TXT'.format(DXC_PACKAGE), 'DXC-{0}/LICENSE.TXT'.format(DXC_VERSION))
shutil.copy2('.packages/_win/bin/x64/dxcompiler.dll', 'DXC-{0}/lib/win64/'.format(DXC_VERSION))
try:
  shutil.copytree('{0}/include/dxc'.format(DXC_PACKAGE), 'DXC-{0}/include/dxc'.format(DXC_VERSION), dirs_exist_ok=True, ignore_dangling_symlinks=True)
except TypeError as e:
  shutil.copytree('{0}/include/dxc'.format(DXC_PACKAGE), 'DXC-{0}/include/dxc'.format(DXC_VERSION), ignore_dangling_symlinks=True)
except OSError as e:
  print('Ignoring OSError {0}'.format(e))

print('Basic folder prepared: DXC-{0}/include'.format(DXC_VERSION))
print('Build linux64 and macosx libraries using ./s2_build_linux64.sh and ./s2_build_macosx.sh\n  (places results to ..lib/linux64 and ..lib/macosx)')
print('And run ./s3_make_package.sh to finally get .tar.gz for upload')
