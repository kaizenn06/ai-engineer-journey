class Matrix :
    def __init__(self, n, m, a) :
        self.n = n
        self.m = m
        self.a = a
    def multiply(self, other) :
        result = Matrix(self.n, other.m, [[0] * other.m for _ in range(self.n)])
        for i in range(self.n) :
            for j in range(other.m) :
                for k in range(other.n) :
                    result.a[i][j] += self.a[i][k] * other.a[k][j]
        return result
    def __str__(self) :
        return '\n'.join(' '.join(map(str, row)) for row in self.a)

if __name__ == '__main__' :
    t = int(input())
    for _ in range(t) :
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(n)]
        b = [[a[i][j] for i in range(n)] for j in range(m)]
        A = Matrix(n, m, a)
        B = Matrix(m, n , b)
        C = A.multiply(B)
        print(C)