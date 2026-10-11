from math import gcd

class Point :
    def __init__(self, tu, mau) :
        self.tu = tu
        self.mau = mau
    def rutgon(self) :
        ucln = gcd(self.tu, self.mau)
        self.tu = self.tu / ucln
        self.mau = self.mau / ucln
        return self
    def __str__(self) :
        return f"{self.tu:.0f}/{self.mau:.0f}"

if __name__ == "__main__" :
    a, b = map(int, input().split())
    x = Point(a, b).rutgon()
    print(x)