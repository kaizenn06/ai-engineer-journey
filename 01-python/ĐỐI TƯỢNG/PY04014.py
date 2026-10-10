class Student :
    def __init__(self, id, name, scores) :
        self.id = f'HS{id:02d}'
        self.name = name
        self.scores = scores
        self.avg = round((self.scores[0] * 2 + self.scores[1] * 2 + sum(self.scores[2:])) / 12 + 1e-9, 1)
        self.rank = self.sieve()

    def sieve(self) :
        if self.avg >= 9 : return "XUAT SAC" 
        elif 8 <= self.avg < 9 : return "GIOI"
        elif 7 <= self.avg < 8 : return "KHA"
        elif 5 <= self.avg < 7 : return "TB"
        else : return "YEU"       

    def __str__(self) :
        return f'{self.id} {self.name} {self.avg:.1f} {self.rank}'

if __name__ == '__main__' :
    n = int(input())
    ds = []
    for i in range(n) :
        name = input()
        scores = list(map(float, input().split())) 
        ds.append(Student(i + 1, name, scores))
    ds.sort(key= lambda x : (-x.avg, x.id))
    for x in ds : 
        print(x)