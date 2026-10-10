if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        s = input()
        c, d = "", 0
        for i in range(len(s)) :
            if c != s[i] :
                if i > 0 : print(d, c, sep = "",end = "")
                c = s[i]
                d = 1
            else :
                d += 1
        print(d, c, sep = "",end = "")
        print()


