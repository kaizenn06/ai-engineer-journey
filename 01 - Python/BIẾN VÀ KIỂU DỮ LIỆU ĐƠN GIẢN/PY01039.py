if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        ok = True
        for i in range(0, len(n), 2) :
            if n[i] != n[0] :
                ok = False
                break
        for i in range(1, len(n), 2) :
            if n[i] != n[1] :
                ok = False
                break
        print("YES" if ok else "NO")
