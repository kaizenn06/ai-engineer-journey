if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        ok = True
        sum = 0
        for i in range(len(n)) :
            if i % 2 == 0 :
                if int(n[i]) % 2 == 1 :
                    ok = False
            else :
                if int(n[i]) % 2 == 0 :
                    ok = False
            sum += int(n[i])
        for i in range(2, sum) :
            if sum % i == 0 :
                ok = False
                break
        print("YES" if ok else "NO")
        
        
