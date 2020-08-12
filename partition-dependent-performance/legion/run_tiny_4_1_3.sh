source /home/jgraham//github/spack/share/spack/setup-env.sh
spack load mpich
spack load boost
spack load lua
export VERSION=mpich_3.3-gcc_8.3.0
export LD_LIBRARY_PATH=/home/jgraham/opt/${VERSION}/lib:/home/jgraham/opt/${VERSION}/lib64:${LD_LIBRARY_PATH}
printenv LD_LIBRARY_PATH
who

mpiexec -n 12 /home/jgraham/github/flecsale/build-${VERSION}/apps/hydro/3d/hydro_3d -m /home/jgraham/github/instructions/meshes/26x78x130on12_4_1_3/26x78x130.g.012 -- -ll:cpu 2 -ll:gsize 0 –l:show_rsrv –ll:csize 3500 |& tee tiny_4_1_3.out

who

