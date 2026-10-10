if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        mul = 1
        for i in range(len(n)) :
            if n[i] == '0' :
                continue
            mul *= int(n[i])
        print(mul)
