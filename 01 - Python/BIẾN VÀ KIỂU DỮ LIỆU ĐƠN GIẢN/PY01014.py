from math import ceil
a, K, N = map(int, input().split())
t = ceil(a / K)
found = False
while True :
    res = K * t - a
    if K * t <= N and res > 0: 
        found = True
        print(res, end = " ")
    if K * t > N : break
    res += K
    t += 1
if found == False : print(-1)
