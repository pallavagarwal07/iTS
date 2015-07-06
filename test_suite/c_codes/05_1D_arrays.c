#include <stdio.h>
int arr[10];
int main()
{
    int arr2[15];
    int i;
    for(i=0; i<10; i++)
        arr[i] = 1;
    for(i=0; i<15; i++)
        arr2[i] = i*2;

    for(i=0; i<10; i++)
        printf("%d\t", arr[i]*2);
    printf("\n");
    for(i=0; i<15; i++)
        printf("%d\t", arr2[i]/2);

    return 0;

}
