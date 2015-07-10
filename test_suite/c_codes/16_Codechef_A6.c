#include<stdio.h>
#include<string.h>
#define MAX 494
#define valueof(c) (a[(c)]-'0')
char a[MAX];
char b[100];
void fillbit(){
    int i=0;
    a[i]='0';
    for(i=1;i<MAX;i++)
        a[i]=(valueof(i-(i&-i))^1+'0');
}

int lms[100];
int last=0;

int pos;
int lmsutil(int n){
    lms[0]=0;
    int i,len=0;
    for(i=1;i<n;)
    {
        if(b[i]==b[len])
        {
            len++;
            lms[i]=len;
            i++;
        }
        else
        {
            if(len==0)
            {
                lms[i]=0;
                i++;
            }
            else
            {
                len=lms[len-1];
            }
        }
    }
}

int kmp(int n){
    int len;
    len=MAX;
    lmsutil(n);
    int counter=0;
    int x=0,y=0,flag=0;
    while(y<n+1)
    {
        if(a[x]==b[y])
        {
            {
                if(y==counter)
                {
                    printf("%d ",x-y);
                    counter++;
                }
                x=x+1;
                y=y+1;
            }
            if(y==n+1)
            {
                break;
            }
        }
        else if(y==0)
            x=x+1;
        else
        {
            y=lms[y-1];
        }
        if(x==len-1)
        {
            break;
            flag=1;
        }
    }
    for(;counter<n+1;counter++)
        printf("%d ",-1);

    return flag;
}

void solve(int n){
    kmp(n);

}

int main(){
    int t;
    fillbit();
    int temp,flag=1,count,check;
    scanf("%d",&t);
    int s;
    while(t--)
    {flag=1;count=0;temp=-1;
        int p,i,x;
        s=0;
        check=1;
        scanf("%d",&p);
        for(i=0;i<p;i++)
        {
            scanf("%d",&x);
            if(flag)
            {
                if(temp==x)
                    count++;
                else
                {
                    count=1;
                    temp=x;
                }

                if (count==3)
                {
                    flag=0;
                }

                b[i]=x?1+'0':0+'0';
            }
            if(flag==0)
            {
                if(check)
                {

                    s=kmp(i-1);
                    printf("%d ",-1);
                }

                else
                {

                    printf("%d ",-1);
                }
                check=0;
            }
        }
        if(check==1)
        {
            kmp(i-1);
        }
        printf("\n");
    }
    return 0;
}
