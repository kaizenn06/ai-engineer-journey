if __name__ == "__main__" :
    s = input()
    n = len(s)
    t = s[n - 3] + s[n - 2] + s[n - 1]
    t = t.lower()
    print("yes" if t == ".py" else "no")
         
        
