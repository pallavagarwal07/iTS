#include <stdio.h>

int main()
{
    int
        arr[5][4] = {
            {1,2,3},
            {2,3},
            {6,7,8}
        };
    int arr2[][
        7
    ]
        = {
            {2,arr[1][1]*54,5,6},
            {1,2,34,5,9}
        };
    int arr3[][3][5] = {
        {
            {
                3
            }
        },
        {
            {
                3
            }
        }
    };
    int i,j,k;

    for(i=0; i<5; i++)
    {
        for(j=0; j<4; j++)
            printf("%d\t", arr[i][j]);
        printf("\n");
    }
    printf("\n");

    for(i=0; i<2; i++)
    {
        for(j=0; j<7; j++) printf("%d\t",
                arr2[i][j]);
        printf(
                "\n"
                );
    }
    printf(
            "\n"
            );

    for(i=0;
            i<2; i++)
    {
        for
            (j=0; j<3; j++)
        {
            for(k=0; k<5; k++) printf("%d,", arr3[i][j][k]); printf("\t"); } printf("\n"); } printf("\n"); return 0;
}
