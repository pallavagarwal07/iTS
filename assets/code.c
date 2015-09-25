#include <stdio.h>
int main()
{
	int i =10;
	while(i--)
	{
		_DEBUG_(i > 5);
		printf("Hello World.\n");
	}
	return 0;
}
