class Customer :
    def __init__(self, id, name, type, old, new) :
        self.id = f'KH{id:02d}'
        self.name = name
        self.type = type
        self.num = new - old
        self.limit = 100 if type == 'A' else 500 if type == 'B' else 200
        self.money_in = min(self.num, self.limit) * 450
        self.money_out = max(0, self.num - self.limit) * 1000
        self.vat = self.money_out // 20
        self.total_pay = self.money_in + self.money_out + self.vat

    def __str__(self) :
        return f"{self.id} {self.name} {self.money_in} {self.money_out} {self.vat} {self.total_pay}"


if __name__ == '__main__' :
    n = int(input())
    a = []
    for i in range(n) :
        name = ' '.join(input().strip().split()).title()
        type, old, new = input().split()
        a.append(Customer(i + 1, name, type, int(old), int(new)))
    a.sort(key= lambda x : -x.total_pay)
    print(*a, sep= '\n')