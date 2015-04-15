#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)
int main()
{
    int d;
    s(d);
    int num = 0, i=0;
    while(d>0)
    {
        int a=1, k=0;
        for(k=0; k<i; k++)
        a = a * 10;
        num = num + (d&1)*a;
        //func(a);
        //printf("%d %d %d\n", num, a, d);
        d = d/2;
        i = i + 1;
    }
    printf("%d\n", num);
    return 0;
}
/*
inline void func(int a)
{
    printf("%d", a);
}
/*

#include<stdio.h>
int main()
{
    int c,n,t;
    scanf("%d",&t);
    while(t--)
    {
        c=0;
        scanf("%d",&n);
        while(n>=5)
        {
            n=n/5;
            c=c+n;

        }
        printf("%d\n",c);
    }
    return 0;
}*/