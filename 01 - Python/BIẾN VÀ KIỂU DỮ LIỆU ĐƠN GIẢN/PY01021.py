if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        s = input()
        res, sum = "", 0
        for i in range(len(s)) :
            if s[i] >= '0' and s[i] <= '9' :
                sum += int(s[i])
            else : res += s[i]
        res = ''.join(sorted(res))
        res += str(sum)
        print(res)


