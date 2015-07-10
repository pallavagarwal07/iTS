#include<stdio.h>


#define s(n) scanf("%lld",&n)
#define ll long long int
#define INF 10000009
ll C[4004];

ll min(ll a, ll b)
{
    if(a<b)
        return a;
    else
        return b;
}

ll max(ll a, ll b)
{
    if(a<b)
        return b;
    else
        return a;
}

void update(ll ss, ll se, ll qs, ll qe, ll val, ll x)
{
    if(ss == qs && se == qe)
    {   
        C[x]=min(C[x], val);
        return;
    }
    ll m = (ss + se)/2;
    if(qe <= m)
        update(ss, m, qs, qe, val, 2*x);
    else if(qs > m)
        update(m+1, se, qs, qe, val, 2*x+1);
    else
    {
        update(ss, m, qs, m, val, 2*x);
        update(m+1, se, m+1, qe, val, 2*x+1);
    }
}

ll query(ll ss, ll se, ll q, ll x)
{
    if(ss == se && ss == q)
        return C[x];
    ll m = (ss + se)/2;
    if(q<=m)
        return min(C[x], query(ss, m, q, 2*x));
    else
        return min(C[x], query(m+1, se, q, 2*x+1));
}

int main()
{
    ll T, j, N, K, M, A[1001], l, r, c, temp, K1[1001], K2[1001], T1[501], T2[501], len, sum, i;
    s(T);
    while(T--)
    {
        s(N);
        s(K);
        s(M);
        for(i=0;i<4004;i++)
            C[i]=INF;
        for(i=0;i<N;i++)
            s(A[i]);
        for(i=0;i<M;i++)
        {
            s(l);
            s(r);
            s(c);
            update(1,N,l,r,c,1);
        }
        j=0;
        sum=0;
        for(i=0;i<N;i++)
        {
            sum+=A[i];
            if(A[i]<0)
            {
                temp = query(1,N,i+1,1);
                if(temp!=INF)
                {
                    K1[j]=0-A[i];
                    K2[j++]=temp;
                    //printf("%lld %lld\n", K1[j-1], K2[j-1]);
                }
            }   
        }
        //Knapsack
        len = j;
        for(i=0;i<=K;i++)
        {
            T1[i]=0;
            T2[i]=0;
        }
        for(i=0;i<len;i++)
        {
            T2[0]=0;
            for(j=1;j<=K;j++)
            {
                if(K2[i]<=j)
                    T2[j]=max(T1[j], T1[j-K2[i]]+K1[i]);
                else
                    T2[j]=T1[j];
                //cout<<"T2["<<j<<"] = "<<T2[j]<<" and T1[j] = "<<T1[j]<<endl;
            }
            for(j=0;j<=K;j++)
                T1[j]=T2[j];
        }
        printf("%lld\n", sum+T1[K]);
    }
    return 0;
}

/*#include <stdio.h>*/

/*#define s(n) scanf("%d",&n)*/

/*int main()*/
/*{*/
    /*int n, i, j;*/
    /*char a[10][100];*/
    /*s(n);*/
    /*for(i=0;i<n;i++)*/
    /*{*/
        /*scanf("%s",a[i]);*/
    /*}*/
    /*for(i=0;i<n;i++)*/
    /*{*/
        /*for(j=0;a[i][j]!='\0';j++)*/
        /*{*/
            /*if('a'<=a[i][j] && a[i][j]<='z')*/
                /*a[i][j]-=('a'-'A');*/
        /*}*/
    /*}*/
    /*for(i=0;i<n;i++)*/
        /*printf("%s\n",a[i]);*/
    /*return 0;*/
/*}*/

/*#include <stdio.h>*/
/*#include <math.h>*/
/*int main()*/
/*{*/
    /*char a;*/
    /*int b;*/
    /*float c;*/
    /*char d[10];*/
    /*int e[10];*/
    /*scanf("%c %d %f %s", &a, &e[0], &c, d);*/
    /*printf("%f", fabs(c));*/
    /*printf("%d\t %s %s %f",e[0],d,&(d[1]),c);*/
    /*return 0;*/
/*}*/

/*#include <stdio.h>*/


/*int main()*/
/*{*/
    /*char a;*/
    /*int b;*/
    /*float c;*/
    /*char d[10];*/
    /*int e[10];*/
    /*scanf("%c %d %f %s", &a,&b,&c,d);*/
    /*printf("Yo");*/
    
    /*int a[11], b[11]={1,2,3}, i, j;*/
    /*for(i=0, j=1;j*i<=110;++j, i++)*/
    /*{*/
        /*a[i]=i*j;*/
        /*b[j-1]+=b[5];*/
        /*b[j-1]%=2;*/
    /*}*/
    /*for(i=0; i<11; i++)*/
        /*printf("%d\t", a[i]);*/
    /*printf("\n");*/
    /*for(i=0; i<11; i++)*/
        /*printf("%d\t", b[i]);*/
    /*printf("\n");*/

    /*i=0;*/
    /*while(i<11)*/
    /*{*/
        /*printf("%d ", a[i]);*/
        /*switch(a[i]%10)*/
        /*{*/
            /*case 0:*/
            /*case 1:*/
            /*case 2:*/
            /*case 3:*/
                /*printf("wohoo, less than 4!\n");*/
            /*case 7:*/
            /*case 8:*/
                /*printf("Weird :/\n");*/
                /*break;*/
            /*default:*/
                /*if (a[i]%2==0)*/
                    /*printf("Now we are even :D\n");*/
                /*else*/
                    /*printf("This is odd\n");*/
        /*}*/
        /*i++;*/
    /*}*/
    /*printf("While over!\n");*/
    /*j=0;*/


    /*for(i=0; i<11; i++)*/
        /*printf("%d\t", a[i]);*/
    /*printf("\n");*/

    /*for(i=0; i<11; i++)*/
        /*printf("%d\t", b[i]);*/
    /*printf("\n");*/


    /*do*/
    /*{*/
        /*++b[j++];*/
    /*}while(j<i);*/

    /*for(i=0; i<11; i++)*/
        /*printf("%d\t", a[i]);*/
    /*printf("\n");*/

    /*for(i=0; i<11; i++)*/
        /*printf("%d\t", b[i]);*/
    /*printf("\n");*/
/*#include <stdio.h>*/

/*int main()*/
/*{*/
    /*int lol;*/
    /*float se;*/
    /*char ssd;*/
    /*scanf("%11d %22Lf %c",&lol,&sw,&ssd);*/
    /*return 0;*/
/*}*/
