if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n, b = map(int, input().split())
        s = ""
        while n != 0 :
            temp = n % b
            if temp > 9 :
                temp = chr(ord('A') + temp - 10)
            s += str(temp)
            n //= b
        print(s[::-1])

        
