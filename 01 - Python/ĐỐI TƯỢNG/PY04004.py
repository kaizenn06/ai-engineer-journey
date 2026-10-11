from math import gcd

class Point :
    def __init__(self, tu, mau) :
        self.tu = tu
        self.mau = mau
    def add(self, other) :
        self.tu = (self.tu * other.mau) + (other.tu * self.mau)
        self.mau = self.mau * other.mau
        return self
    def rutgon(self) :
        ucln = gcd(self.tu, self.mau)
        self.tu = self.tu / ucln
        self.mau = self.mau / ucln
        return self
    def __str__(self) :
        return f"{self.tu:.0f}/{self.mau:.0f}"

if __name__ == "__main__" :
    a, b, c, d = map(int, input().split())
    x, y = Point(a, b), Point(c, d)
    z = Point.add(x, y).rutgon()
    print(z)

