class Candidate :
    def __init__(self, id, name, lt, th) :
        self.id = 'TS0' + str(id)
        self.name = name
        self.lt = lt / 10.0 if lt > 10.0 else lt
        self.th = th / 10.0 if th > 10.0 else th
        self.avg = (self.lt + self.th) / 2
        self.static = "TRUOT" if self.avg < 5 else "CAN NHAC" if self.avg < 8 else "DAT" if self.avg < 9.5 else "XUAT SAC"                         

    def __str__(self) :
        return f"{self.id} {self.name} {self.avg:.2f} {self.static}"

if __name__ == "__main__" :
    n = int(input()) 
    a = []
    for i in range(n) :
        a.append(Candidate(i + 1, input(), float(input()), float(input())))
    a.sort(key= lambda x : -x.avg)
    print(*a, sep='\n')