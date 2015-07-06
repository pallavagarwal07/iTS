#include <stdio.h>

int main()
{
    int i = 10;
    int j = 20;
    int k = i++ + ++j - ++i;
    j = k++ + --j;
    printf("%d %d %d\n", i, j, k);
    return 0;
}
