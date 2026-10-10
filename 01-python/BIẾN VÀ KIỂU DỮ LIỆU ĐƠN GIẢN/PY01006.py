t = int(input())
while t > 0 :
    n = list(map(int, input()))
    check = True
    for i in range(0, len(n)) :
        if n[i] != 4 and n[i] != 7 :
            check = False
    print("YES" if check else "NO")
    t -= 1
