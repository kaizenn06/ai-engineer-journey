def isPrime(n) :
    if n < 2 : return False
    for i in range(2, n) :
        if n % i == 0 :
            return False
    return True

if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        s = input()
        n = int(s) % 10000
        print("YES" if isPrime(n) else "NO")
        
        
