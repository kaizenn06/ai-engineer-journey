if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = int(input())
        start = 1 if n % 2 == 1 else 2
        s = 0
        for i in range(start, n + 1, 2) :
            s += 1 / i
        print(f"{s:.6f}")
