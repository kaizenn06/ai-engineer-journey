if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        ok = True
        for i in range(2, len(n)) :
            if len(n) % i == 0 :
                ok = False
                break
        d1, d2 = 0, 0
        for i in range(len(n)) :
            if n[i] == '2' or n[i] == '3' or n[i] == '5' or n[i] == '7':
                d1 += 1
            else : 
                d2 += 1
        if d1 < d2 : ok = False
        print("YES" if ok else "NO")
