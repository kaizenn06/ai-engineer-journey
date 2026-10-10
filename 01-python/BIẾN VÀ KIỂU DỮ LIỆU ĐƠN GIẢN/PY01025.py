if __name__ == "__main__" :
    n = input()
    a = []
    while len(n) > 3 :
        a.append(n[-3:])
        n = n[:-3]
    a.append(n)
    print(",".join(a[::-1]))
