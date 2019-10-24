# FleCSALE build instructions (darwin non-spack version)

## Load modules

```
module load cmake git mpich/3.2.1-gcc_8.2.0 boost/1.67.0
```

## Build and install flecsi-third-party

```
git clone --recursive git@github.com:laristra/flecsi-third-party.git
cd flecsi-third-party; mkdir build; cd build
export VERSION="scaling"
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/opt/$VERSION -DCMAKE_BUILD_TYPE=Release -DLEGION_USE_CUDA=OFF -DLEGION_USE_HDF5=OFF -DLEGION_USE_OPENMP=ON -DENABLE_CALIPER=OFF -DGASNet_CONDUIT=ibv
make -j
make install
```

## Build and run flecsale

```
cd ../..
git clone --recursive https://github.com/laristra/flecsale.git --single-branch
export CMAKE_PREFIX_PATH=$HOME/opt/$VERSION
cd flecsale; mkdir build; cd build
cmake .. -DENABLE_UNIT_TESTS=OFF -DCMAKE_BUILD_TYPE=Release -DFLECSI_RUNTIME_MODEL=legion -DENABLE_CALIPER=OFF
make -j
cd apps/hydro/2d/
mpirun -n 2 ./hydro_2d -m ../../../../data/meshes/square_32x32.g
cd ../../maire_hydro/2d/
mpirun -n 2 ./maire_hydro_2d -m ../../../../data/meshes/square_32x32.g
```