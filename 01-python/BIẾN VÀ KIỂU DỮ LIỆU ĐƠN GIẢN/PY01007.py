t = int(input())
while t > 0 :
    a = list(map(float, input().split()))
    i = 1
    while True :
        if a[0] * (1 + a[1] / 100) ** i >= a[2]:
            print(i)
            break
        i += 1
    t -= 1
