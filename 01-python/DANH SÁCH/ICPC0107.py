def change(x, p, q) :
    return x.replace(str(p), str(q))

if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        p, q = map(int, input().split())
        x1 = input().strip()
        if ' ' in x1:
            x1, x2 = x1.split()
        else:
            x2 = input().strip()
        mn = min(p, q)
        mx = max(p, q)
        a = int(change(x1, mx, mn)) + int(change(x2, mx, mn))
        b = int(change(x1, mn, mx)) + int(change(x2, mn, mx))
        print(a, b)
