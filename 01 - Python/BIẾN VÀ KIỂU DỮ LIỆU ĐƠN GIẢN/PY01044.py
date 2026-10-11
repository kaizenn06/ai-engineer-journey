if __name__ == "__main__" :
    s1 = set(input().lower().split())
    s2 = set(input().lower().split())
    print(*sorted(s1 | s2))
    print(*sorted(s1 & s2))
    
    
