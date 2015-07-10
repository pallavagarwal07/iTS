#include <stdio.h>
int main()
{
    char a;
    int b;
    float c;
    char d[10];
    int e[10];
    scanf("%c %d %f %s", &a, &e[0], &c, d);
    printf("%d\t %s %s %f",e[0],d,&(d[1]),c);
    return 0;
}
