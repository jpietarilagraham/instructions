source /home/jgraham//github/spack/share/spack/setup-env.sh
spack load mpich
spack load boost
spack load lua
export VERSION=mpich_3.3-gcc_8.3.0
export LD_LIBRARY_PATH=/home/jgraham/opt/${VERSION}/lib:/home/jgraham/opt/${VERSION}/lib64:${LD_LIBRARY_PATH}
printenv LD_LIBRARY_PATH
who

mpiexec -n 64 /home/jgraham/github/flecsale/build-${VERSION}/apps/hydro/2d/hydro_2d -m /home/jgraham/github/instructions/meshes/32x32on32/32x32.g.064 -- -ll:cpu 1 -ll:gsize 0 –ll:show_rsrv –ll:csize 120 |& tee 2d_64.out

who

