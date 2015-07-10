#include <stdio.h>

#define s(n) scanf("%d",&n)

int main()
{
    int n, i, j;
    char a[10][100];
    s(n);
    for(i=0;i<n;i++)
    {
        scanf("%s",a[i]);
    }
    for(i=0;i<n;i++)
    {
        for(j=0;a[i][j]!='\0';j++)
        {
            if('a'<=a[i][j] && a[i][j]<='z')
                a[i][j]-=('a'-'A');
        }
    }
    for(i=0;i<n;i++)
        printf("%s\n",a[i]);
    return 0;
}
