class Customer :
    def __init__(self, id, name, old, new) :
        self.id = f'KH{id:02d}'
        self.name = name
        self.old = old
        self.new = new 
        self.total = self.solve()

    def solve(self) :
        val = self.new - self.old
        if val < 50 : 
            money = val * 100
            return money * (1 + 0.02)
        elif 50 < val < 100 :
            money = (val - 50) * 150 + 50 * 100
            return money * (1 + 0.03)
        else :
            money = (val - 100) * 200 + 50 * 150 + 50 * 100
            return money * (1 + 0.05)

    def __str__(self) :
        return f'{self.id} {self.name} {self.total:.0f}'

if __name__ == '__main__' :
    n = int(input())
    a = []
    for i in range(n) : 
        a.append(Customer(i + 1, input(), int(input()), int(input())))
    a.sort(key= lambda x : -x.total)
    for x in a :
        print(x)