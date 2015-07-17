#include <stdio.h>

long long func(int arr[54]);

int main()
{
    int arr[54], i;
    for(i=0; i<54; i++)
        arr[i] = i;

    printf("%d\n", func(arr));

    for(i=0; i<27; i++)
        printf("%d\t", arr[i]);
    printf("\n");
    for(i=27; i<54; i++)
        printf("%d\t", arr[i]);
    printf("\n");
    return 0;
}

long long func(int arr[54])
{
    int i;
    for(i=0; i<54; i++)
        arr[i] *= 2;
    return 100;
}
