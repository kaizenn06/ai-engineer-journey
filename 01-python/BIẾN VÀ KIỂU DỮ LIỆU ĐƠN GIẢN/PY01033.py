from math import gcd 
if __name__ == "__main__" :
    l, r = map(int, input().split())
    for i in range(l, r - 1) :
        for j in range(i + 1, r) :
            for k in range(j + 1, r + 1) :
                if gcd(i, j) == gcd(j, k) == gcd(i, k) == 1:
                    print(f"({i}, {j}, {k})")
