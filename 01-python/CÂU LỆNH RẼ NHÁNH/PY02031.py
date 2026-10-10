def isPrime(n) :
    for i in range(2, n) :
        if n % i == 0 :
            return False
    return n > 1

if __name__ == "__main__" : 
    n, m = map(int, input().split())
    a = []
    for _ in range(n) :
        row = list(map(int, input().split()))
        a.append(row)
    for i in range(n) :
        for j in range(m) :
            print("1" if isPrime(a[i][j]) else "0", end = " ")
        print()
