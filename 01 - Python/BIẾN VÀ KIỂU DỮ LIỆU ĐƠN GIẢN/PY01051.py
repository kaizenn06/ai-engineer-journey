if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        sum = 0
        for i in range(len(n)) :
            sum += int(n[i])
        if sum != int(str(sum)[::-1]) or len(str(sum)) <= 1:
            print("NO")
        else : 
            print("YES")
