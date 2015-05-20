#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)

int func(int a, int b);

int main()
{
    long long a=1;
    a=10*a;
    int i=0;
    int b= 5;
    for(i=2; i<=a; i++)    
    {
        printf("%d\n", 10*sizeof(long long)); 
        printf("One of the factors is\n");
    }
    printf("%d\n ", func(a, b));

    return 0;
}

int func(int a, int b)
{
    int j=0;
    printf("This function was executed successfully\n");
    return (a+b);
}
