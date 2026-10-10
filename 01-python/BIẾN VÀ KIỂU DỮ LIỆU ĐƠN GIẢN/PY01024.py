if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        sum, ok = 0, True
        for i in range(len(n)) :
            sum += int(n[i])
        for i in range(len(n) - 1) :
            if abs(ord(n[i]) - ord(n[i + 1])) != 2 :
                ok = False
                break
        print("YES" if ok and sum % 10 == 0 else "NO")


