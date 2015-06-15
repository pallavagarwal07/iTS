#include <stdio.h>

int toBinary(int a)
{
    int t = 0, l = 1;
    while(a > 0)
    {
        t += l*(a%2);
        a /= 2;
        l *= 10;
    }
    return t;
}

int main()
{
    int a;
    scanf("%d", &a);
    int bin = toBinary(a);
    printf("The binary is: %d\n", bin);
    return 0;
}
