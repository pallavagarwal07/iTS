#include <stdio.h>
#include <stdlib.h>
int a=5;
long double b=7;
int main()
{
printf("%d : %Lf \n", a, b);
int a=10;
b = b+3;
printf("%d : %LF \n", a, b);
return 0;
}

