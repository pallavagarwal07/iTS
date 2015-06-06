#include <stdio.h>
#include <stdlib.h>
#define s(n) scanf("%d",&n)
int l, b;
int arr[100][100];

void print()
{
    int i, j;
    for(i=0; i<=l; i++)
    {
        for(j=0; j<=b; j++)
        {
            printf("%8d ", arr[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int fibo(int a, int b)
{
    if(b > a/2)
        return fibo(a, a-b);
    if(a<0 || b<0 || a<b)
        return 0;
    if(a == b || b == 0)
        return 1;
    if(arr[a][b] != -1)
    {
        return arr[a][b];
    }
    int k = fibo(a-1, b) + fibo(a-1, b-1);
    arr[a][b] = k;
    print();
    return k;
}

int main()
{
    s(l);
    s(b);
    int i, j;
    for(i=0; i<=50; i++)
    {
        for(j=0; j<=50; j++)
        {
            arr[i][j] = -1;
        }
    }
    printf("%d\n", fibo(l,b));
}
