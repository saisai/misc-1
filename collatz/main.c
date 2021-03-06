/*
    How to run this C program:
    $ gcc -Wall -O3 main.c
    $ ./a.out
*/
#include <stdio.h>
#include <sys/types.h>


int main(void)
{
    long long unsigned int i, n, m;

    m = 0;
    for (i = 3; i < 67108864; i+=2) {
        n = i;
        while (n >= i) {
            n = n % 2 ? 3 * n + 1 : n / 2;
            if (n > m)
                m = n;
        }
    }

    printf("%3lld\n", m);

    return 0;
}
