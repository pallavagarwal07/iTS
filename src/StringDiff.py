arr = []

def Dif(str1, str2):
    m = len(str2)
    n = len(str1)
    i = 0
    j = 0
    while i<=n:
        arr[0][i] = i
        i += 1
    while j<=m:
        arr[j][0] = j
        j += 1
    i = 1
    j = 1
    while i <= n:
        j = 1
        while j <= m:
            if str2[j-1] == str1[i-1]:
                arr[j][i] = arr[j-1][i-1]
            else:
                arr[j][i] = min(arr[j-1][i], arr[j][i-1]) + 1
            j += 1
        i += 1
    return arr[m][n]

#def Dif(str1, str2):
    #if arr[len(str2)][len(str1)] != 999999:
        #return arr[len(str2)][len(str1)]
    #if len(str1) == 0:
        #arr[len(str2)][len(str1)] = len(str2)
        #return len(str2)
    #if len(str2) == 0:
        #arr[len(str2)][len(str1)] = len(str1)
        #return len(str1)
    #if str1[-1] == str2[-1]:
        #k = Dif(str1[:len(str1)-1], str2[:len(str2)-1])
        #arr[len(str2)][len(str1)] = k
        #return k
    #k = min(Dif(str1, str2[:len(str2)-1]), Dif(str1[:len(str1)-1], str2)) + 1
    #arr[len(str2)][len(str1)] = k
    #return k


def print_arr(str2, str1, arr):
    print("\t0\t",)
    for a in range(1, len(arr[0])):
        print(str1[a-1]+"\t",)
    print('')
    for i, a in enumerate(arr):
        print(str2[i-1] if i>0 else '0', "\t",)
        for b in a:
            print(str(b) + "\t",)
        print('')
    print('\n\n')

stack = {}

def init(str2, str1):
    len1 = len(str1)+1
    len2 = len(str2)+1
    global arr
    arr = [999999]*len2
    for i in range(0, len2):
        arr[i] = [999999]*len1

    Dif(str1, str2)
    i = len2 - 1
    j = len1 - 1


    while i > 1 and j > 1:
        k = sorted([[arr[i-1][j], (i-1, j)], [arr[i][j-1], (i, j-1)], [arr[i-1][j-1], (i-1, j-1)]])
        k = k[0][1]
        i, j = k
        stack[i] = j

def getIndex(str2, str1, index):
    return stack[index+1]-1

