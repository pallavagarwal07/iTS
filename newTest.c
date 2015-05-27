#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)

int main()
{
    int a[2][3];
    a[0][0] = 4;
    a[1][3] = 5;
    printf("%d %d\n", a[0][0], a[1][3]);
    return 0;
}
