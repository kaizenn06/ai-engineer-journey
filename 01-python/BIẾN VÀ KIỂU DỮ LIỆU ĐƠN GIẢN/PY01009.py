s = input()
lower = upper = 0
for i in range(0, len(s)) :
    if s[i].islower() : lower += 1
    if s[i].isupper() : upper += 1
s = s.lower() if lower >= upper else s.upper()
print(s)
