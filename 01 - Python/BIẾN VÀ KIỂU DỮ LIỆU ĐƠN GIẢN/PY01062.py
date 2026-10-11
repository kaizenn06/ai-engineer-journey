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
        isdigit, isprime = 0, 0
        for i in range(len(n)) :
            if isPrime(int(n[i])) :
                isprime += 1
        isdigit = len(n) - isprime
        print("YES" if isPrime(len(n)) and isprime > isdigit else "NO")
        
        
