if __name__ == "__main__" :
    t = int(input())
    for _ in range(t) :
        n, d = map(int, input().split())
        a = [x for x in input().split()]
        print(" ".join(a[d:]), " ".join(a[:d])) 
            
