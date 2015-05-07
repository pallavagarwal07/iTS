#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)


int func(int a, int b);
int main()
{
    int c;
    c = func(4, 2)*32;
    printf("%d\n", c);
}
int func(int a, int b)
{
    int j;
    s(j);
    printf("This function was executed successfully\n");
    return j*b;
}



/*
long func(int b)
{
    printf("%d %d\n", b, b);
}
long double func2__();
long double func2__(double a, int g);
long double func2__()
{
    printf("hELLO wORLD");
}
int func2__(int overload)
{
    scanf("%d", &a);
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

long double func2__(double a, int g)
{
    printf("Please Work!!!\n");
}
*/