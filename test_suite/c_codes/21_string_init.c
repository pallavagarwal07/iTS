#include <stdio.h>

int main()
{
    char *d = "Hip Hip Hurray!";
    printf("%c\n", d[1]);
    int i=0;
    for(i=0; d[i] != '\0'; i++)
    {
        printf("%c", d[i]);
    }
    printf("\n");
    return 0;
}
