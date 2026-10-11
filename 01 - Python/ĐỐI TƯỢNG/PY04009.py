class SoPhuc :
    def __init__(self, a, b) :
        self.a = a
        self.b = b

    def add(self, other) :
        a = self.a + other.a
        b = self.b + other.b
        return SoPhuc(a, b)

    def multiply(self, other) :
        a = self.a * other.a - (self.b * other.b)
        b = self.a * other.b + self.b * other.a
        return SoPhuc(a, b)

    def __str__(self) :
        return f'{self.a} + {self.b}i' if self.b > 0 else f'{self.a} - {abs(self.b)}i'

if __name__ == '__main__' :
    t = int(input())
    for _ in range(t) :
        a, b, c, d = map(int, input().split())
        A = SoPhuc(a, b)
        B = SoPhuc(c, d)
        C = A.add(B).multiply(A)
        D = A.add(B).multiply(A.add(B))
        print(f'{C}, {D}')