#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)

int isPrime(int a)
{
    int flag=1;
    int i=2;
    if(a%i==0 && i<a)
    {
        return 0;
    }
    printf("Now checking for %d \n", a);
    for(i=3; i<a/2 && flag; i+=2)
    {
        if(a%i == 0)
            flag = 0;
    }
    return flag;
}

int main()
{
    long long a;
    scanf("%lld\n", &a);
    int i=0;
    for(i=2; i<=a; i++)
    {
        if(isPrime(i) && a%i==0)
        {
            printf("One of the factors is %d.\n", i);
        }
    }
    return 0;
}





/*
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
