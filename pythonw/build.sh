#!/bin/bash -e -x

PREFIX=$HOME/python

cc -I${PREFIX}/include/python2.7 -g -fwrapv -O3 -Wall \
    -arch x86_64 -L${PREFIX}/lib -lpython2.7 -o pythonw pythonw.c

install_name_tool -change libpython2.7.dylib \
    @loader_path/../../python/lib/libpython2.7.dylib ./pythonw
otool -L ./pythonw

./pythonw -V
