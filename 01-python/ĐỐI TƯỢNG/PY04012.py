class SinhVien :
    def __init__(self, msv, name, lop) :
        self.msv = msv
        self.name = name
        self.lop = lop

class Static :
    def __init__(self, msv, stt, sv) :
        self.msv = msv
        self.stt = stt
        self.sv = sv
        v = stt.count('v')
        m = stt.count('m')
        d = 10 - v * 2 - m * 1
        self.diem = d if d > 0 else 0
        self.tt = "KDDK" if self.diem == 0 else ""

    def __str__(self) :
        return f'{self.msv} {self.sv.name} {self.sv.lop} {self.diem} {self.tt}'

if __name__ == '__main__' :
    n = int(input())
    sv = {}
    ds = {}
    for _ in range(n) :
        msv = input()
        name = input()
        lop = input()
        sv[msv] = SinhVien(msv, name, lop)
    for _ in range(n) :
        msv, stt = input().split()
        ds[msv] = Static(msv, stt, sv[msv])
    for msv in sv :
        print(ds[msv])
