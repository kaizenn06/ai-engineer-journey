if __name__ == "__main__" :
    n = input()
    ok = True
    i = 0
    while i < len(n) :
        if n[i] != '6' :
            ok = False
            break
        if i + 2 < len(n) and n[i:i + 3] == '688' :
            i += 3
        elif i + 1 < len(n) and n[i:i + 2] == '68' :
            i += 2
        else : i += 1
    print("YES" if ok else "NO")
