from datetime import datetime

class Movies :
    def __init__(self, id, type_movie, day, name, num) :
        self.id = f'P{id:03d}'
        self.type_movie = type_movie
        self.day = datetime.strptime(day, '%d/%m/%Y')
        self.name = name
        self.num = num

    def __str__(self) :
        return f"{self.id} {self.type_movie} {self.day:%d/%m/%Y} {self.name} {self.num}"
 
if __name__ == "__main__" :
    n, m = map(int, input().split())
    a, b = {}, []
    for i in range(n) :
        id = f'TL{i + 1:03d}'
        name = input()
        a[id] = name
    for i in range(m) :
        b.append(Movies(i + 1, a[input()], input(), input(), int(input())))
    b.sort(key= lambda x : (x.day, x.name, -x.num))
    print(*b, sep='\n')

