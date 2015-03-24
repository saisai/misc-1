#include <stdio.h>
#include <string.h>


int main()
{
    int i;
    char f[] = "aaaaaaaaaaaaaaaaaa";

    strncpy(f + 2, "1234", 4);

    for (i = 0; i < 10; i++)
        printf("%d '%c' %d\n", i, *(f + i), *(f + i));

    return 0;
}
