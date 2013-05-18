#include <stdio.h>


int main(void)
{
    float f;
    double x;
    long double y;
    int i;
    void *p;
    unsigned char c;

    f = 25.0;
    f = 3.4028234E38;
    p = &f;
    printf("float: %ld\n", sizeof(f));
    for (i = 3; i >= 0; i--) {
        c = *(char *)(p + i);
        printf("%d %x\n", i, c);
    }

    x = 2.2250738585072009E-308;
    x = 4.9406564584124654E-324;
    x = 1.7976931348623157E308;
    x = 1.0;
    p = &x;
    printf("double: %ld\n", sizeof(x));
    for (i = 7; i >= 0; i--) {
        c = *(char *)(p + i);
        printf("%d %x\n", i, c);
    }

    y = 1.0;
    y = 1.0 / 3.0;
    printf("%Lf\n", y);
    p = &y;
    printf("long double: %ld\n", sizeof(y));
    for (i = 15; i >= 0; i--) {
        c = *(char *)(p + i);
        printf("%d %x\n", i, c);
    }

    return 0;
}
