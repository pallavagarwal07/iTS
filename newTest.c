#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)
int main()
{
    int i=0;
    int k=3;
    int j = &k;
    for(i=0; i<10; i++)
    {
        int k = 4;
        printf("%d %d\n", k, *j);
        *j += 1;

    }
    printf("%d\n", k);
}

// Bug 1 --i + --i