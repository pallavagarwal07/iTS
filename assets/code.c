#include <stdio.h>

int main()
{
    printf("Hello World!!\n");
    char* c, b, * a;
    b = 'a';
    c=&b;
    a=c;
    int d = *c;
    printf("%c %d %c", *a, b, *c);
    return 0;
}
