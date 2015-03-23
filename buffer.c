#include <stdio.h>

#include <stdlib.h>



int a=5;




long double b=7;




int main()


{


    scanf("%d", &b);


    printf("%d : %.3Lf\n", a, b);


    int a=10;


    scanf("%d %d", &a, &b);


    b = b+3+(10==10)+ (a=6) + (3|   4);


    printf("%d : %LF \n", a, b);


    return 0;



}


