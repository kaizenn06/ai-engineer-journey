n = list(map(int, input()))
d = 0
for i in range(0, len(n)) :
    if n[i] == 4 or n[i] == 7 : 
        d += 1
print("YES" if d == 4 or d == 7 else "NO")
