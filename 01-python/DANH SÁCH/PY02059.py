def isPrime(n) :
	for i in range(2, int(n ** 0.5) + 1) :
		if n % i == 0 :
			return False
	return n > 1

if __name__ == "__main__" :
	n, m = map(int, input().split())
	a = list(list(map(int, input().split())) for _ in range(n))
	maxPrime = max((a[i][j] for i in range(n) for j in range(m) if isPrime(a[i][j])), default=-1)
	if maxPrime == -1 :
		print("NOT FOUND")
	else :
		print(maxPrime)
		pos = [(i, j) for i in range(n) for j in range(m) if a[i][j] == maxPrime]
		for (i, j) in pos :
			print(f"Vi tri [{i}][{j}]")
