if __name__ == "__main__" :
    n = input()
    d = 0
    while len(n) > 1 :
        sum = 0
        d += 1
        for i in range(len(n)) :
            sum += ord(n[i]) - ord('0')
        n = str(sum)
    print(d)


