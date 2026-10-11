def tong(n) :
	return sum(map(int, n))
if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = int(input())
		a = list(input().split())
		a.sort(key=lambda x: (tong(x), int(x)))
		print(" ".join(a))
	
