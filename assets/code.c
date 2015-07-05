#include <stdio.h>

int main()
{
    int a;
    a=70;
    float b;
    b = ((float)a/20)*40;
    printf("%f\n", b);
    a = (long)b/100;
    printf("The binary is: %c\n", (char)a);
    return 0;
}
