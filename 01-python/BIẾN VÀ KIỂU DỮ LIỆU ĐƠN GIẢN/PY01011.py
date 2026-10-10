def sinh() :
    ans = []
    for a in [2, 4, 6, 8] :
        x = a * 10 + a
        ans.append(x)
    for a in [2, 4, 6, 8] :
        for b in [0, 2, 4, 6, 8] :
            x = a * 1000 + b * 100 + b * 10 + a
            ans.append(x)
    for a in [2, 4, 6, 8]:
        for b in [0, 2, 4, 6, 8]:
            for c in [0, 2, 4, 6, 8]:
                x = a * 100000 + b * 10000 + c * 1000 + c * 100 + b * 10 + a
                ans.append(x)
    return ans

ans = sinh()
ans.sort()

t = int(input())    
while t > 0 :
    n = int(input())
    for x in ans :
        if x >= n : break
        print(x, end = " ")
    print()
    t -= 1
