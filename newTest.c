#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)
long func(int b)
{
    printf("%d %d\n", b, b);
}
int main()
{
    int a=0;
    s(a);
    int i=0;int ans = 0;
    int k=1;    while(a>0)
    {




        ans+=(a&1)*k;
        k *= 10;




        a >>= 1;
    }
    printf("%d\n",
     ans);
    return 0;
}

