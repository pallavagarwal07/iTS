#include <stdio.h>

int main()
{
    int i = 10;
    int j_b = 20;
    int k = (i++) + (++j_b) - (++i) + (-j_b);
    j_b = (k++) + (--j_b);
    printf("%d %d %d\n", i, j_b, k);
    return 0;
}
