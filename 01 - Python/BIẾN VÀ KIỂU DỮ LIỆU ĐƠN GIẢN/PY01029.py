from math import gcd
if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        print("YES" if gcd(int(n), int(n[::-1])) == 1 else "NO")
