#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)
int main() {
    int i, j;
    for(i=0;i<=5;i=i+1)
    {
    for(j=0;j<5-i;j=j+1)
    printf(" ");
    for(j=0;j<2*i+1;j=j+1)
    printf("*");
    printf("\n");
    }
    return 0;
}
