#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)
int main()
{
    int a;
    s(a);
    int i=0;
    int ans = 0;
    int k=1;
    while(a>0)
    {
        ans += (a & 1)*k;
        k *= 10;
        a >>= 1;
    }
    printf("%d\n", ans);
    return 0;
}

// Bug 1 --i + --i