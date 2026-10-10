def isPrime(n) :
	for i in range(2, int(n ** 0.5) + 1) :
		if n % i == 0 : 
			return False
	return n > 1

if __name__ == "__main__" :
	n = int(input())
	a = list(map(int, input().split()))
	b = [x for x in a if isPrime(x)]
	b = sorted(b)
	idx = 0
	for i in range(n) :
		if not isPrime(a[i]) : continue
		a[i] = b[idx]
		idx += 1
	print(" ".join(str(x) for x in a))
