class SinhVien :
    def __init__(self, id, name, d1, d2, d3) :
        self.id = f"SV{id:02d}"
        self.name = ' '.join(list(name.split())).title()
        self.avg = round(((d1 * 3 + d2 * 3 + d3 * 2) / 8) + 1e-9, 2)

    def __str__(self) :
        return f"{self.id} {self.name} {self.avg:.2f}"

if __name__ == "__main__" :
    n = int(input())
    a = []
    for i in range(n) :
        a.append(SinhVien(i + 1, input().strip(), int(input()), int(input()), int(input())))
    a.sort(key= lambda x : (-x.avg, x.id))
    rank = 1
    i = 0
    while i < len(a):
        j = i
        while j < len(a) and a[j].avg == a[i].avg:
            print(a[j], rank)
            j += 1
        rank += j - i
        i = j
        