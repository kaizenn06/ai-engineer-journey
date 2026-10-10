if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        s = input()
        for i in range(len(s)) :
            if s[i] >= '1' and s[i] <= '9' :
                x = int(s[i])
                for _ in range(x) :
                    print(s[i - 1], end = "")
        print()
