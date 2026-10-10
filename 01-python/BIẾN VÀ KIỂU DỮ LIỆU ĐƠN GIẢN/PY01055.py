if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        ok = True 
        if len(n) % 2 == 0 or n[0] == n[1]: 
            print("NO")
            continue
        for i in range(2, len(n), 2) :
            if n[i] != n[0] :
                ok = False
                break
        print("YES" if ok else "NO")
        
        
