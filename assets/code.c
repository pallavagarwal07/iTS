#include <stdio.h>

#define s(n) scanf("%d",&n)

long long func(int x, long long y)
{
    return (long long)x + 10;
}

int main()
{
    int n, i;
    int a=69, b;
    b=0;
    n=10;
    for(i=0;i<n;i++)
    {
        b = b + a + 1000000000000 + func(a, a);
    }
    for(i=0;i<n;i++)
        printf("%d\n",a+func(i, i));
    return 0;
}
