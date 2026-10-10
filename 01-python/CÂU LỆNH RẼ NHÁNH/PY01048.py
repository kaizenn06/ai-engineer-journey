if __name__ == "__main__" : 
    t = int(input())
    for _ in range(t) :
        n = int(input())
        d, k = 0, 2
        while k * (k + 1) // 2 <= n :
            x = n - k * (k - 1) // 2
            if x % k == 0 :
                d += 1
            k += 1
        print(d)

