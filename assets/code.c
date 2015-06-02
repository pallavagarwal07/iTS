#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)
int main()
{
    int *a;
    int b= 10;
    a = &b;
    printf("%d\n", *a);
    return 0;
}
/*int num = -1, a[10000];*/
/*int get(int p)*/
/*{*/
    /*if(num == -1)*/
    /*{*/
        /*a[0] = 1;*/
        /*a[1] = 1;*/
        /*int i;*/
        /*for(i=2; a[i-1]<p; i++)*/
            /*a[i] = a[i-1]+a[i-2];*/
        /*i -= 2;*/
        /*num = i;*/
        /*return a[num];*/
    /*}*/
    /*else*/
    /*{*/
        /*while(a[num] > p)*/
            /*num--;*/
        /*return a[num];*/
    /*}*/
/*}*/
/*int main()*/
/*{*/
    /*int k = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000;*/
    /*while(k > 0)*/
    /*{*/
        /*int l = get(k);*/
        /*k -= l;*/
        /*printf("%d\n", l);*/
    /*}*/
    /*return 0;*/
/*}*/
