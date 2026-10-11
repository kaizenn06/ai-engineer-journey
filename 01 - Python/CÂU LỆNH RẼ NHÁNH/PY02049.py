if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n, p = map(int, input().split())
        x = 0
        while n > 0 :
            n //= p
            x += n
        print(x)
