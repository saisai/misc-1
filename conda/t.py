import os
import sys
from time import sleep
from subprocess import call


def main():
    call(['git', 'pull'])
    sleep(5)
    if sys.platform == 'win32':
        call([os.environ['COMSPEC'], '/c', 'bld.bat'])
    else:
        call(['bash', 'build.sh'])
    sleep(10 * 60)


if __name__ == '__main__':
    while 1:
        main()
