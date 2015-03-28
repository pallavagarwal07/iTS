#include <stdio.h>
#include <stdlib.h>
int a=5;
long double b=7;
int main()
{
scanf("%d", &b);
printf("%d : %.3Lf\n", a, b);
int a=10;
scanf("%d %d", &a, &b);
printf("I hope this breaks :P\n");
printf("Yes! a nested brace\n");
printf("May this not be printed\n");
b = b+3+(10==10)+ (a=6) + (3| 4);
printf("%d : %LF \n", a, b);
return 0;
}

