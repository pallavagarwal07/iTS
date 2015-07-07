/*#include <stdio.h>*/

/*int main()*/
/*{*/
    /*int a=5, v,  d=4, e[5]={1,2,3,4,5}, f[2][3]={{1,2,3},{4,5,6}};*/
    /*int a;*/
    /*printf("%d %d", e[2], f[1][1]);*/
    /*scanf("%d", &a);*/
    /*long long t;*/
    /*float m;*/
    /*scanf("%lld %f", &t, &m);*/
    /*a += 3;*/
    /*t += 30000;*/
    /*m += a;*/
    /*printf("%d\t%lld\n%f\n", a, t, m);*/
    /*return 0;*/
/*}*/
#include <stdio.h>
int main()
{
    /*int arr[11] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};*/
    /*printf("%d\n", arr[3]);*/
    /*char arr2[5] = {'a', 'b', 'c', 'd', 'e'};*/
    /*printf("%c\n", arr2[2]);*/
        int a[2][2][2]={{{1,2}}};
        printf("%d\n", a[0][1][0]);
        int b[] = {2,3};
        int c[][3]={{1,2,3},{4,5,6}};
        printf("%d\n", c[1][2]);
    return 0;
}
