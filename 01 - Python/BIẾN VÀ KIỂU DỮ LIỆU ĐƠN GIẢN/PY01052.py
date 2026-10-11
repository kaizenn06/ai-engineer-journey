if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        ok, sum = True, 0
        for i in range(len(n)) :
            sum += int(n[i])
        for i in range(2, sum) :
            if sum % i == 0 :
                ok = False
                break
        print("YES" if ok else "NO")
