#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)

int func(int a);

int main()
{
    int a = 400000000000000000000000009000000000000000000000000000000000000;
    while(a>0)
    {
        int n = func(a);
        printf("%d\n", n);
        a -= n;
    }
    return 0;
}

int func(int a)
{
    int i = 1;
    int j = 1;
    while(j<=a)
    {
        int t = i+j;
        i = j;
        j = t;
    }
    return i;
}
