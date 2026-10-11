from datetime import datetime

class Cuarow :
    def __init__(self, id, name, unit, end) :
        self.id = id
        self.name = name
        self.unit = unit
        self.start = datetime.strptime('6:00', '%H:%M')
        self.end = datetime.strptime(end, '%H:%M')
        self.v = 120 / ((self.end - self.start).total_seconds() / 3600)

    def __str__(self) :
        return f"{self.id} {self.name} {self.unit} {round(self.v)} Km/h"

if __name__ == '__main__' :
    n = int(input())
    a = []
    for i in range(n) :
        id = ""
        name = input()
        unit = input()
        end = input().strip()
        id += ''.join(x[0].upper() for x in unit.split())
        id += ''.join(x[0].upper() for x in name.split())
        a.append(Cuarow(id, name, unit, end))
    a.sort(key= lambda x : -x.v)
    print(*a, sep= "\n")