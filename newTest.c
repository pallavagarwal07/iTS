#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)
int main()
{
    int i=0;
    int k= 4;
    k = - --i + - --i;
    printf("%d %d\n", i, k);
}

// Bug 1 --i + --i