/*#include <stdio.h>*/

/*int main()*/
/*{*/
    /*int a = 4;*/
    /*a++;*/
    /*++a;*/
    /*switch (a)*/
    /*{*/
           /*case a>0?4:3: printf("That's not right!\n");int b;*/
                /*break;*/
        /*case 15: printf("Nope, not this either.\n");*/
                /*break;*/
        /*case 6: printf("Yep, you got it!!\n");{int c=10; printf("%d",c*c);}*/
                /*break;*/
        /*case 7: printf("too far, bro, too far.\n");*/
                /*break;*/
        /*default: printf("Seriously?!\n");*/
    /*}*/
    /*printf("\n");*/

    /*switch (a)*/
    /*{*/
        /*case 4: printf("That's not right!\n");*/
        /*case 5: printf("Nope, not this either.\n");*/
        /*case 6: printf("Yep, you got it!!\n");*/
        /*case 7: printf("too far, bro, too far.\n");*/
        /*default: printf("Seriously?!\n");*/
    /*}*/
    /*printf("\n");*/

    /*switch (a)*/
    /*{*/
        /*default: printf("Seriously?!\n");*/
        /*case 4: printf("That's not right!\n");*/
        /*case 5: printf("Nope, not this either.\n");*/
        /*case 6: printf("Yep, you got it!!\n");*/
        /*case 7: printf("too far, bro, too far.\n");*/
    /*}*/
    /*printf("\n");*/

    /*switch (a)*/
    /*{*/
        /*default: printf("Seriously?!\n");*/
        /*case 4: printf("That's not right!\n");*/
        /*case 5: printf("Nope, not this either.\n");*/
        /*case 7: printf("too far, bro, too far.\n");*/
    /*}*/
    /*printf("\n");*/

    /*return 0;*/
/*/*/
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
    j=0;
    printf("While over!");
    do
    {
        a[j] = a[j/2] + ++b[j++];
    }while(j<i);
    printf("Do While over!");
    for(j=0;j<(int)23.0/2;j++)
        printf("%d %d", a[j], b[j]);

    return 0;
}
//*}*/
