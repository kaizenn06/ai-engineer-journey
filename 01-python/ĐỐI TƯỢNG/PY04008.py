import sys

class Matrix:
    def __init__(self, n, m, a):
        self.n = n
        self.m = m
        self.a = a

    def multiply(self, other):
        result = Matrix(self.n,other.m,[[0] * other.m for _ in range(self.n)])
        for i in range(self.n):
            for j in range(other.m):
                for k in range(self.m):
                    result.a[i][j] += self.a[i][k] * other.a[k][j]
        return result
    
    def __str__(self):
        return '\n'.join(' '.join(map(str, row)) for row in self.a)


if __name__ == '__main__':
    data = sys.stdin.read().split()
    pos = 0
    t = int(data[pos])
    pos += 1
    for _ in range(t):
        n = int(data[pos])
        m = int(data[pos + 1])
        pos += 2
        a = []
        for i in range(n):
            row = list(map(int, data[pos:pos + m]))
            pos += m
            a.append(row)
        b = [[a[i][j] for i in range(n)] for j in range(m)]
        A = Matrix(n, m, a)
        B = Matrix(m, n, b)
        C = A.multiply(B)
        print(C)