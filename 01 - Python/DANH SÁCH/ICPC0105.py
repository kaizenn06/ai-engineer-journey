if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        s = input()
        n = len(s)
        a = []
        digit = ""
        m = -1
        for c in s :
            if c.isdigit() :
                digit += c
            else :
                if digit != "" :
                    a.append(digit)
                    m = max(m, int(digit))
                    digit = ""
        if digit != "" :
            m = max(m, int(digit))
        print(m)
