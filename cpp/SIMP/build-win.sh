#! /bin/bash -e

# Check that valid parameters have been specified.
if [ $# -ne 2 ] || ([ "$1" != "14" ] && [ "$1" != "12" ]) || ([ "$2" != "Debug" ] && [ "$2" != "Release" ])
then
  echo "Usage: build-win.sh {14|12} {Debug|Release}"
  exit
fi

# Check that msbuild is on the system path.
./require-msbuild.sh

cd 3rdParty

./extract-Eigen-3.2.2.sh
cd ..

echo "[SIMP C++] Building..."

if [ ! -d build ]
then
  mkdir build
  cd build

  # Note: We need to configure twice to handle conditional building.
  echo "[SIMP C++] ...Configuring using CMake..."
  cmake -G "Visual Studio $1 Win64" ..
  cmake ..

  cd ..
fi

cd build

echo "[SIMP C++] ...Running build..."
cmd //c "msbuild /p:Configuration=$2 simp.sln"

echo "[SIMP C++] ...Finished building SIMP C++."
