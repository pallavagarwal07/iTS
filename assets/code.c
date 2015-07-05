#include <stdio.h>

int main()
{
    int a;
    a=70;
    float b;
    b = ((float)a/20)*40;
    b = a==70? 3 + 8:4 + 6==6?3:8;
    printf("%f\n", b);
    a = (long)b/100;
    return 0;
}
