#include <stdio.h>

int main()
{
    int a[11], b[11]={1,2,3}, i, j;
    for(i=0, j=1;j*i<=110;++j, i++)
    {
        a[i]=i*j;
        b[j-1]+=b[5];
        b[j-1]%=2;
    }
    for(i=0; i<11; i++)
        printf("%d\t", a[i]);
    printf("\n");
    for(i=0; i<11; i++)
        printf("%d\t", b[i]);
    printf("\n");

    i=0;
    while(i<11)
    {
        printf("%d ", a[i]);
        switch(a[i]%10)
        {
            case 0:
            case 1:
            case 2:
            case 3:
                printf("wohoo, less than 4!\n");
            case 7:
            case 8:
                printf("Weird :/\n");
                break;
            default:
                if (a[i]%2==0)
                    printf("Now we are even :D\n");
                else
                    printf("This is odd\n");
        }
        i++;
    }
    printf("While over!\n");
    j=0;


    for(i=0; i<11; i++)
        printf("%d\t", a[i]);
    printf("\n");

    for(i=0; i<11; i++)
        printf("%d\t", b[i]);
    printf("\n");


    do
    {
        printf("J is : %d\n", j);
        ++b[j++];
        printf("J is : %d\n", j);
    }while(j<i);
    return 0;
}
