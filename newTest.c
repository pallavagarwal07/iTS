#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)

int main()
{
    int i=0;
    for(i=0; i<15; i++)
    {
        printf("%d Hello World\n", i);
        if(i == 5)
            break;
    }
    printf("Out of the loop !! ");
}
