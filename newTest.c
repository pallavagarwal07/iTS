#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)

int func(int a);

int main()
{
    long long a=1;
    a=10*a;
    int i=0;

    for(i=2; i<=a; i++)    {
        printf("%d\n", 10*sizeof(     long    long   )); printf("One of the factors is\n");
        a=5/0;
    }
    printf("%d\n ", func(a));
    int j=5/0;

    return 0;
}

int func(int a)
{
    int j=0;
  //  j = a+b^a;
    printf("This function was executed successfully\n");
    return (++j)*a;
}
