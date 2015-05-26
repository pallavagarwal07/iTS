#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)

int main()
{
    int *a, b;
    b = sizeof(int*);
    a = &b;
    printf("%d\n", *a);
}
