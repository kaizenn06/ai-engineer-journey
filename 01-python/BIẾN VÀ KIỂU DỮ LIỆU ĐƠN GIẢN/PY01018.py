if __name__ == "__main__" :
    P = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ_.")
    while True:
        a = input().split()
        if a[0] == "0": break
        k, s = int(a[0]), a[1]
        t = ""
        for i in range(len(s)) :
            t += P[(P.index(s[i]) + int(k)) % 28]
        t = t[::-1]
        print(t)


