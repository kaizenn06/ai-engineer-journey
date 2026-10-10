from math import gcd
def isPrime(n) :
    if n < 2 : return 0
    for i in range(2, n) :
        if n % i == 0 : return 0
    return 1

t = int(input())
for _ in range(t) :
    a, b = map(int, input().split())
    c = str(gcd(a, b))
    sum = 0
    for i in range(len(c)) :
        sum += int(c[i])
    print("YES" if isPrime(sum) else "NO")
