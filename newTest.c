#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)

int func(int a, int b);

int main()
{
    int a = 9, b=4;
    printf("%d \n", func(a, b));
    return 0;
}

int func(int a, int b)
{
    if(b > a)
        return 0;
    if(a == b)
        return 1;
    if(b == 0)
        return 1;
    return func(a-1, b) + func(a-1, b-1);
}
