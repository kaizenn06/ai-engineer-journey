class Invoice :
    def __init__(self, id, name, quantity, price, discount) :
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.discount = discount
        self.money = self.quantity * self.price - self.discount

    def __str__(self) :
        return f"{self.id} {self.name} {self.quantity} {self.price} {self.discount} {self.money}"

if __name__ == "__main__" :
    n = int(input())
    a = []
    for i in range(n) :
        a.append(Invoice(input(), input(), int(input()), int(input()), int(input())))
    a.sort(key= lambda x : -x.money)
    print(*a, sep="\n")