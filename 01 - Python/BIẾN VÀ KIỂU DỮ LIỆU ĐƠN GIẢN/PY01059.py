import math
if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n = input()
        add, mul = 0, 1
        add = sum(int(n[i]) for i in range(0, len(n), 2))
        # tao 1 list a chua cac so khac o o vi tri le
        a = [int(n[i]) for i in range(1, len(n), 2) if n[i] != '0']
        mul = math.prod(a) if a else 0
        print(add, mul)
        
        
