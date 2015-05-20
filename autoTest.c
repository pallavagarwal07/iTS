#include <stdio.h>
#include <stdlib.h>

int main() 
{
	int k1, k2, k3, k4, k5, n=0, u, l;
	    
	    scanf("%d %d %d %d %d",&k1,&k2,&k3,&k4,&k5);
	    u=k1+100;
	    l=k1;
	    n= (k2>=l && k2<=u)+(k3>=l && k3<=u)+(k4>=l && k4<=u);
	    printf("%d",n);
	    
	return 0;
}
