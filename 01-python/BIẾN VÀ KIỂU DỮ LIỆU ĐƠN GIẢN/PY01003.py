t = int(input())
while t > 0 :
    n = list(input())
    for i in range(len(n) - 1, 0, -1) :
        if len(n) != 1 :
            if int(n[i]) >= 5 :
                n[i] = '0'
                n[i - 1] = str(int(n[i - 1]) + 1)
            else :
                n[i] = '0'
    print("".join(n))
    t -= 1
