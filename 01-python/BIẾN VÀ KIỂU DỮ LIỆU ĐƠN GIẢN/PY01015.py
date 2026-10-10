if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        s = input()
        found = True
        for i in range(len(s) - 1) :
            if s[i] > s[i + 1] :
                found = False
                break
        print("YES" if found == True else "NO")
