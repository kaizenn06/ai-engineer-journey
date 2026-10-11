from math import sqrt

class Point :
    def __init__(self, x, y) :
        self.x = x
        self.y = y
    def distance(self, other) :
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)    

class Triangle :
    def __init__(self, p1, p2, p3) :
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    def solve(self) :
        a = self.p1.distance(self.p2)
        b = self.p1.distance(self.p3)
        c = self.p2.distance(self.p3)
        if max(a, b, c) * 2 >= a + b + c:
            print("INVALID")
        else:
            print("{:.3f}".format(a + b + c))

if __name__ == "__main__" :
    t = int(input())
    a = []
    i = 0
    for _ in range(t) : 
        a += [float(x) for x in input().split()]
    for _ in range(t) :
        X = Triangle(Point(a[i], a[i + 1]), Point(a[i + 2], a[i + 3]), Point(a[i + 4], a[i + 5]))
        X.solve()
        i += 6