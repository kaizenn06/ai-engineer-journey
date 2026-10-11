from math import comb
if __name__ == "__main__" :
    n = int(input())
    a = []
    for i in range(n) :
        a.append(input())
    d = 0
    row = [0] * n
    col = [0] * n
    for i in range(n) :
        for j in range(n) :
            if a[i][j] == 'C' :
                row[i] += 1
                col[j] += 1
    for i in range(n) :
        d += comb(row[i], 2)
        d += comb(col[i], 2)
    print(d)
