#include <stdio.h>

void func(int x);

int new_func()
{
    printf("Let's test something basic...\n");
    return 69;
}

int main()
{
    /*func(1);*/
    printf("%d",new_func());
    return 0;
}

void func(int alpha)
{
    printf("X there, Alpha here! WOW _/\\_\n");
    return;
}
