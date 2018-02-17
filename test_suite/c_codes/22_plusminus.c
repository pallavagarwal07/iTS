
#include <stdio.h>

int main() {
    int x,y; float z; char ch;
    x=1, y=4, z=8, ch='5';

    printf("%d ", 4/y+x );
    printf("%2.2f ", x/y*0.5 );
    printf("%c ", x*=y+ch ); 
    printf("%d ", y+++-x );
    printf("%d ", y+++--x );
    printf("%f ", (!z, z) );
    printf("%d ", z>y>x );

    return 0;
}
