from math import gcd

def isPrime(n) :
    if n < 2:
        return 0
    for i in range(2, n) :
        if n % i == 0 : 
            return 0
    return 1

t = int(input())
while t > 0 :
    n = int(input())
    d = 0
    for i in range(1, n) :
        if gcd(n, i) == 1:
            d += 1
    print("YES" if isPrime(d) else "NO")
    t -= 1
