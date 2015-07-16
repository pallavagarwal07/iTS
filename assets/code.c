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
    printf("Update called with %lld %lld %lld %lld %lld %lld\n", ss, se, qs, qe, val, x);
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
    ll T, j, N, K, M, A[1001], l, r, c, temp, K3[1001], K2[1001], T1[501], T2[501], len, sum, i;
    printf("All Declarations Done\n");
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
            printf("Everything was scanned successfully\n");
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
                    K3[j]=0-A[i];
                    K2[j++]=temp;
                    printf("%lld", K2[j-1]);
                    /*printf("%lld %lld\n", K3[j-1], K2[j-1]);*/
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
                    T2[j]=max(T1[j], T1[j-K2[i]]+K3[i]);
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
