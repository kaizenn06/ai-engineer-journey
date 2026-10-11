def sinh() :
    ans = []
    for i in [2, 4, 6, 8] :
        x = i * 10 + i
        ans.append(x)
    for i in [2, 4, 6, 8] :
        for j in [0, 2, 4, 6, 8] :
            x = i * 1000 + j * 100 + j * 10 + i
            ans.append(x)
    for i in [2, 4, 6, 8] :
        for j in [0, 2, 4, 6, 8] :
            for k in [0, 2, 4, 6, 8] :
                x = i * 100000 + j * 10000 + k * 1000 + k * 100 + j * 10 + i
                ans.append(x)
    return ans

ans = sinh()

if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = int(input())
        for i in ans :
            if i < n : print(i, end = " ")
        print()
