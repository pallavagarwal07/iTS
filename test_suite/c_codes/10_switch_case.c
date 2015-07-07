#include <stdio.h>

int main()
{
    int a = 4;
    a++;
    ++a;
    switch (a)
    {
        case 4: printf("That's not right!\n");
                break;
        case 5: printf("Nope, not this either.\n");
                break;
        case 6: printf("Yep, you got it!!\n");
                break;
        case 7: printf("too far, bro, too far.\n");
                break;
        default: printf("Seriously?!\n");
    }
    printf("\n");

    switch (a)
    {
        printf("Never print this\n");
        case 4: printf("That's not right!\n");
        case 5: printf("Nope, not this either.\n");
        case 6: printf("Yep, you got it!!\n");
        case 7: printf("too far, bro, too far.\n");
        default: printf("Seriously?!\n");
    }
    printf("\n");

    switch (a)
    {
        default: printf("Seriously?!\n");
        case 4: printf("That's not right!\n");
        case 5: printf("Nope, not this either.\n");
        case 6: printf("Yep, you got it!!\n");
        case 7: printf("too far, bro, too far.\n");
    }
    printf("\n");

    switch (a)
    {
        default: printf("Seriously?!\n");
        case 4: printf("That's not right!\n");
        case 5: printf("Nope, not this either.\n");
        case 7: printf("too far, bro, too far.\n");
    }
    printf("\n");

    return 0;
}
