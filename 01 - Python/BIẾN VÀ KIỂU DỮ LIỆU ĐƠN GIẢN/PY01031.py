if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n, b = map(int, input().split())
        s = ""
        while n != 0 :
            x = n % b
            if x < 10 :
                s += str(x)
            else : s += chr(ord('A') + x - 10)
            n //= b
        print(s[::-1])
