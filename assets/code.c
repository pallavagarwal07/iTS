/*#include <stdio.h>*/

/*int main()*/
/*{*/
    /*int a[11], b[11]={1,2,3}, i, j;*/
    /*for(i=0, j=1;j*i<=110;++j, i++)*/
    /*{*/
        /*a[i]=i*j;*/
        /*b[j-1]+=b[5];*/
        /*b[j-1]%=2;*/
    /*}*/
    /*i=0;*/
    /*while(i<11)*/
    /*{*/
        /*printf("%d ", a[i]);*/
        /*switch(a[i]%10)*/
        /*{*/
            /*case 0:*/
            /*case 1:*/
            /*case 2:*/
            /*case 3:*/
                /*printf("wohoo, less than 4!\n");*/
            /*case 7:*/
            /*case 8:*/
                /*printf("Weird :/\n");*/
                /*break;*/
            /*default:*/
                /*if (a[i]%2==0)*/
                    /*printf("Now we are even :D\n");*/
                /*else*/
                    /*printf("This is odd\n");*/
        /*}*/
        /*i++;*/
    /*}*/
    /*printf("While over!");*/
    /*j=0;*/
    /*do*/
    /*{*/
        /*a[j] = a[j/2] + ++b[j++];*/
    /*}while(j<i-3);*/
    /*for(j=0;j<23/2;j++)*/
        /*printf("%d %d", a[j], b[j]);*/

    /*return 0;*/
/*}*/
#include <stdio.h>

int main()
{
    int a;
    scanf("%d", &a);
    long long t;
    float m;
    scanf("%lld %f", &t, &m);
    a += 3;
    t += 30000;
    m += t;
    printf("%d\t%5.7lld\n%f\n", a, t, m);
    return 0;
}
