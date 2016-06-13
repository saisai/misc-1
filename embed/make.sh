#!/bin/bash

rm ./a.out

PP=$HOME/python

gcc -I $PP/include/python2.7 -L $PP/lib -l python2.7 main.c

export DYLD_LIBRARY_PATH=$PP/lib
export PASSPHRASE=PassW0rd
./a.out $PP/bin/python
