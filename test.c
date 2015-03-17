#include     <stdio.h>
#include <stdlib.h>

int        a = 5, b=13, h=  145 ;
float k=1;
int func();  

int main(   )    
{
    printf   ("Hello %d\n  World!!%d\n",a, b    );      func(); //This is a comment
    return 0;
}

int func()/*This is 
a 
multiline
comment*/{

    int r=   8*a;
    int b=a = 14.3; //Sorry another comment
/*Another multiline*/
 /*comment*/
 /*Yo!DEBUGMODE*/
    a=6;
    double k=30*45;
    printf("I'm here!\n");
}
