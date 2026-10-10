def isPrime(n) :
    if n < 2 : return False
    for i in range(2, n) :
        if n % i == 0 :
            return False
    return True

if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        ok = True
        for i in range(len(n)) :
            if isPrime(i) :
                if not isPrime(int(n[i])) :
                    ok = False
                    break
            else :
                if isPrime(int(n[i])) :
                    ok = False
                    break
        print("YES" if ok else "NO")
        
        
