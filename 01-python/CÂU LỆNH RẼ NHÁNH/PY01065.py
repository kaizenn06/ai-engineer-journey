def check(n, s) :
    for i in range(len(n)) :
        if s[i] != '?' and s[i] != n[i] :
            return False
    return True

if __name__ == "__main__" : 
    t = int(input())
    for _ in range(t) :
        a, operator, b, equal, c = input().split()
        ok = False
        for i in range(10, 100) :
            if check(str(i), a) :
                for j in range(10, 100) :
                    if check(str(j), b) :
                        for op in ['+', '-', '*', '/'] :
                            if operator != '?' and operator != op : continue
                            if op == '+' :
                                z = i + j
                            elif op == '-' :
                                z = i - j
                            elif op == '*' :
                                z = i * j 
                            else : 
                                if i % j != 0 : continue
                                z = i // j
                            if 10 <= z <= 99 and check(str(z), c) :
                                print(i, op, j, "=", z)
                                ok = True
                                break
                    if ok :
                        break
            if ok :
                break
        if not ok : print("WRONG PROBLEM!")
    

