class SinhVien :
    def __init__(self, name, birthday, d1 ,d2, d3) :
        self.name = name
        self. birthday = birthday
        self.d = d1 + d2 + d3

    def __str__(self) :
        return f'{self.name} {self.birthday} {self.d}'

if __name__ == '__main__' :
    while True :
        try :
            name = input()
            birthday = input()
            d1 = float(input())
            d2 = float(input())
            d3 = float(input())
            print(SinhVien(name, birthday, d1, d2, d3))
        except EOFError :
            break