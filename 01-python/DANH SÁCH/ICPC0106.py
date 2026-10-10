if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        k = int(input())
        n = input()
        if k == 2 :
            print(n)
            continue
        if k == 4 : bit = 2
        elif k == 8 : bit = 3
        else : bit = 4
        while len(n) % bit != 0 :
            n = '0' + n
        res = ""
        for i in range(0, len(n), bit) :
            x = n[i:i + bit]
            val = int(x, 2)
            if val < 10 :
                res += str(val)
            else :
                res += chr(ord('A') + val - 10)
        print(res)
