# FleCSALE build instructions (sapling partial-spack version)

## Required spack packages

```
git clone git@github.com:spack/spack.git
source $HOME/github/spack/share/spack/setup-env.sh
nohup spack install gcc@8.3.0%gcc@8.4.0 2>&1 > gcc8.3.0.build.txt &
spack load gcc; spack compiler find
spack install boost%gcc@8.3.0; spack load boost
spack install cmake%gcc@8.3.0; spack load cmake
spack install lua%gcc@8.3.0; spack load lua
spack install mpich@3.3%gcc@8.3.0; spack load mpich
```

## Build and install flecsi-third-party

```
export VERSION=mpich_3.3-gcc_8.3.0
export CMAKE_PREFIX_PATH=$HOME/opt/$VERSION:$CMAKE_PREFIX_PATH
export LD_LIBRARY_PATH=$HOME/opt/$VERSION/lib:$HOME/opt/$VERSION/lib64:$LD_LIBRARY_PATH
git clone --recursive https://github.com/laristra/flecsi-third-party.git
cd flecsi-third-party; mkdir build-$VERSION
cd legion; git checkout -b control_replication origin/control_replication
cd ../../build-$VERSION
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/opt/$VERSION -DCMAKE_BUILD_TYPE=Release -DENABLE_CALIPER=OFF -DCMAKE_C_FLAGS=-g -DCMAKE_CXX_FLAGS=-g
make –j; make install
```

## Build and test flecsale

```
cd ../..
git clone --recursive https://github.com/laristra/flecsale.git
cd flecsale; mkdir build-$VERSION; cd build-$VERSION
cmake .. -DENABLE_UNIT_TESTS=ON -DCMAKE_BUILD_TYPE=Release -DFLECSI_RUNTIME_MODEL=legion -DENABLE_CALIPER=OFF -DCMAKE_C_FLAGS=-g -DCMAKE_CXX_FLAGS=-g -DENABLE_FLECSI_TUTORIAL=OFF
make -j
ctest
```

## Create a mesh

```
mpiexec -n 12 $HOME/github/flecsale/build-$VERSION/specializations/apps/make_mesh/make_mesh --dimensions 26 78 130 --partitions 1 2 6 --output-file 26x78x130.g
```

## Run flecsale

```
mpiexec -n 12 $HOME/github/flecsale/build-$VERSION/apps/hydro/3d/hydro_3d -m 26x78x130.g.012 -ll:gsize 0
```
