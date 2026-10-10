if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        ok = True
        if len(n) < 3 :
            print("NO")
            continue
        idx = -1
        for i in range(len(n) - 1) :
            if n[i] > n[i + 1] :
                idx = i
                break
        if idx == -1 : 
            print("NO")
            continue
        for i in range(idx) :
            if n[i] == n[i + 1] :
                ok = False
                break
        for i in range(idx, len(n) - 1) :
            if n[i] <= n[i + 1] :
                ok = False
                break
        print("YES" if ok else "NO")
