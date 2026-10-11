from datetime import datetime

class Exam :
    def __init__(self, stt, id, name, date, hour, group) :
        self.stt = f'T{stt:03d}'
        self.id = id
        self.name = name 
        self.date = datetime.strptime(date, '%d/%m/%Y')
        self.hour = datetime.strptime(hour, '%H:%M')
        self.group = group

    def __str__(self) :
        return f"{self.stt} {self.id} {self.name} {self.date:%d/%m/%Y} {self.hour:%H:%M} {self.group}"

if __name__ == '__main__' :
    n, m = map(int, input().split())
    a, b = {}, []
    for i in range(n) :
        id = input()
        name = input()
        a[id] = name
    for j in range(m) :
        id, date, hour, group = input().split()
        b.append(Exam(j + 1, id, a[id], date, hour, group))
    b.sort(key= lambda x : (x.date, x.hour, x.id))
    print(*b, sep='\n')