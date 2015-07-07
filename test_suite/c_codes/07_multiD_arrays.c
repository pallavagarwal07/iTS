#include <stdio.h>

int main()
{
    int arr[4][7][2];
    int i, j, k;
    for(i=0; i<4; i++)
        for(j=0; j<7; j++)
            for(k=0; k<2; k++)
                arr[i][j][k] = i*j*k;
    for(i=0; i<4; i++)
    {
        for(j=0; j<7; j++)
        {
            for(k=0; k<2; k++)
            {
                printf("%d, ", arr[i][j][k]);
            }
            printf("\t");
        }
        printf("\n");
    }
    return 0;
}
