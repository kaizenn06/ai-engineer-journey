class Teacher :
    def __init__(self, id, name, code, d1, d2) :
        self.id = f'GV{id:02d}'
        self.name = name
        self.code = code
        self.subject = "TOAN" if code[0] == 'A' else 'LY' if code[0] == 'B' else "HOA"
        self.ut = 2 if code[1] == '1' else 1.5 if code[1] == '2' else 1 if code[1] == '3' else 0
        self.d1 = d1 
        self.d2 = d2
        self.total = self.d1 * 2 + self.d2 + self.ut
        self.static = "TRUNG TUYEN" if self.total >= 18 else "LOAI"

    def __str__(self) :
        return f"{self.id} {self.name} {self.subject} {self.total:.1f} {self.static}"

if __name__ == '__main__' :
    n = int(input())
    a = []
    for i in range(n) :
        a.append(Teacher(i + 1, input(), input(), float(input()), float(input())))
    a.sort(key= lambda x : -x.total)
    print(*a, sep= "\n")