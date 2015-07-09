#include <stdio.h>

void func(int);
int main()
{
    func(4);
    return 0;
}
void func(int a){
    printf("Please work! %d\n", a);
}

