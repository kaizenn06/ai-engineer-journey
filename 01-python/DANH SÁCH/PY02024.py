import math
def mul(n) :
	return math.prod(map(int, n))
if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = int(input())
		a = list(input().split())
		a.sort(key=lambda x: (mul(x), int(x)))
		print(" ".join(a))
	
