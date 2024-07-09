#!/bin/bash

set -e

if test $BUILD_PETSC ; then
    if [[ ! -d $HOME/local/petsc/include/petsc ]]; then
	echo "****************************************"
	echo "Building PETSc"
	echo "****************************************"

	git clone -b release https://gitlab.com/petsc/petsc.git petsc --depth=1

	unset PETSC_DIR
	unset PETSC_ARCH

	pushd petsc
	./configure \
	    --with-mpi=yes \
	    --with-precision=double \
	    --with-scalar-type=real \
	    --with-shared-libraries=1 \
	    --with-debugging=0 \
	    {C,CXX,F}OPTFLAGS="-O3" \
	    --prefix=$HOME/local/petsc

	make && make install
	popd

	echo "****************************************"
	echo " Finished building PETSc"
	echo "****************************************"

	echo "****************************************"
	echo "Building SLEPc"
	echo "****************************************"

    git clone -b release https://gitlab.com/slepc/slepc.git slepc --depth=1

    pushd slepc
	unset SLEPC_DIR
	unset SLEPC_ARCH
    PETSC_DIR=$HOME/local/petsc ./configure --prefix=$HOME/local/slepc

    make SLEPC_DIR=$(pwd) PETSC_DIR=$HOME/local/petsc
    make SLEPC_DIR=$(pwd) PETSC_DIR=$HOME/local/petsc install
    popd

	echo "****************************************"
	echo " Finished building SLEPc"
	echo "****************************************"
    else
	echo "****************************************"
	echo " PETSc already installed"
	echo "****************************************"
    fi
else
    echo "****************************************"
    echo " PETSc not requested"
    echo "****************************************"
fi
