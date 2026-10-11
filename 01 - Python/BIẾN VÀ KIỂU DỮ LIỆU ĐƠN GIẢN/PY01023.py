from math import sqrt
if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = int(input())
        print(1, end = " ")
        for i in range(2, int(sqrt(n))) :
            d = 0
            while n % i == 0 :
                d += 1
                n /= i
            if d > 0 : print(f"* {i}^{d}", end = " ")
        if n > 1 : print(f"* {int(n)}^1", end = " ")
        print()


