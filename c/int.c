#include <stdio.h>


int main(void)
{
    int a;
    long b;
    long long c;
    void *p;

    printf("int: %ld\n", sizeof(a));
    printf("long: %ld\n", sizeof(b));
    printf("long long: %ld\n", sizeof(c));
    printf("pointer: %ld\n", sizeof(p));

    return 0;
}
