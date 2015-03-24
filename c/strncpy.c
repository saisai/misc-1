#include <stdio.h>
#include <string.h>


int main()
{
    int i;
    char f[] = "aaaaaaaaaaaa";

    strncpy(f + 2, "123456", 4);

    printf("\"%s\"\n", f);
    for (i = 0; i < 10; i++)
        printf("%d '%c' %d\n", i, f[i], f[i]);

    return 0;
}
