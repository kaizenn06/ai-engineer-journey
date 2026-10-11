class Candidate :
    def __init__(self, id, name, score, nation, area) :
        self.id = f'TS{id:02d}'
        self.name = ' '.join(name.split()).title()
        self.score = score
        self.nation = 0 if nation == 'Kinh' else 1.5
        self.area = 1.5 if area == 1 else 1 if area == 2 else 0
        self.total_score = self.score + self.nation + self.area
        self.static = "Do" if self.total_score >= 20.5 else "Truot"
 
    def __str__(self) :
        return f"{self.id} {self.name} {self.total_score} {self.static}"

if __name__ == '__main__' :
    n = int(input())
    a = []
    for i in range(n) :
        a.append(Candidate(i + 1, input().strip(), float(input()), input(), int(input())))
    a.sort(key= lambda x : (-x.total_score, x.id))
    print(*a, sep='\n')