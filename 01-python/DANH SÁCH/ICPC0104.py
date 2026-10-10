if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        s = input()
        n = len(s)
        a = []
        digit = ""
        m = float('inf')
        for c in s :
            if c.isdigit() :
                digit += c
            else :
                if digit != "" :
                    a.append(digit)
                    m = min(m, int(digit))
                    digit = ""
        if digit != "" :
            m = min(m, int(digit))
        print(m)
