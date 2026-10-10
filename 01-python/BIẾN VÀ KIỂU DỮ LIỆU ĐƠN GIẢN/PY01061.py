def isPrime(n) :
    if n < 2 : return False
    for i in range(2, n) :
        if n % i == 0 :
            return False
    return True

import math
if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        dau = int(n[0] + n[1] + n[2])
        cuoi = int(n) % 1000
        print("YES" if isPrime(dau) and isPrime(cuoi) else "NO")
        
        
