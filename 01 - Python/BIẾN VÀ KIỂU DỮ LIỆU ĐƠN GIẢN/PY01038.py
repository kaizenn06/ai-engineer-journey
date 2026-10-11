if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = int(input())
        i = 0
        found = False
        while i < 1000 :
            if n % 7 == 0 :
                found = True
                print(n)
                break
            rev = int(str(n)[::-1])
            n = n + rev
            i += 1
        if not found : print(-1)
