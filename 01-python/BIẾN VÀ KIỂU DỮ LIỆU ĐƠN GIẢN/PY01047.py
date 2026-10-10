from math import sqrt
if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        s = input()
        n = int(s) % 10000
        if n < 2 :
            print("NO")
            continue
        ok = True
        for i in range(2, int(sqrt(n))) :
            if n % i == 0 :
                ok = False
                break
        print("YES" if ok else "NO")
    
