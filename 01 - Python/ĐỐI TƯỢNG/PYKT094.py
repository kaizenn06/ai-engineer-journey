class Employees :
    def __init__(self, id, name, salary, days, depart) :
        self.id = id
        self.name = name
        self.salary = salary
        self.days = days
        key = id[0]
        val = int(id[1:3])
        match key :
            case 'A' :
                self.hs = 10 if val <= 3 else 12 if val <= 8 else 14 if val <= 15 else 20
            case 'B' :
                self.hs = 10 if val <= 3 else 11 if val <= 8 else 13 if val <= 15 else 16
            case 'C' :
                self.hs = 9 if val <= 3 else 10 if val <= 8 else 12 if val <= 15 else 14
            case 'D' :
                self.hs = 8 if val <= 3 else 9 if val <= 8 else 11 if val <= 15 else 13
        self.money = self.hs * self.salary * self.days
        self.depart = depart

    def __str__(self) :
        return f"{self.id} {self.name} {self.depart} {self.money}000"

if __name__ == '__main__' :
    n = int(input())
    a = []
    department = {}
    for i in range(n) :
        s = input().split()
        id = s[0]
        name = ' '.join(s[1:])
        department[id] = name
    m = int(input())
    for i in range(m) :
        id = input()
        a.append(Employees(id, input(), int(input()), int(input()), department[id[3:]]))
    print(*a, sep= '\n')