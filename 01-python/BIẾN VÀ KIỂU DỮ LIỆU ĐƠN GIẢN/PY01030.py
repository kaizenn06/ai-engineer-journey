from math import gcd
if __name__ == "__main__" :
    n, k = map(int, input().split())
    d = 0
    for i in range(pow(10, k - 1), pow(10, k)) :
        if d == 10 : 
            d = 0
            print()
        if gcd(i, n) == 1 : 
            d += 1
            print(i, end = " ")
