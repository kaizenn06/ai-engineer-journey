from datetime import datetime

class Customer :
    def __init__(self, id, name, room, start, end, fee) :
        self.id = f'KH{id:02d}'
        self.name = name
        self.room = room
        self.start = datetime.strptime(start, "%d/%m/%Y")
        self.end = datetime.strptime(end, "%d/%m/%Y")
        self.days = (self.end - self.start).days + 1
        self.fee = fee
        self.money = self.solve()

    def solve(self) :
        if self.room[0] == '1' : 
            return self.days * 25 + self.fee
        elif self.room[0] == '2' :
            return self.days * 34 + self.fee
        elif self.room[0] == '3' :
            return self.days * 50 + self.fee
        else :
            return self.days * 80 + self.fee

    def __str__(self) :
        return f"{self.id} {self.name} {self.room} {self.days} {self.money}"

if __name__ == '__main__' :
    n = int(input())
    a = []
    for i in range(n) :
        a.append(Customer(i + 1, input(), input(), input().strip(), input().strip(), int(input())))
    a.sort(key= lambda x : -x.money)
    for x in a : 
        print(x)