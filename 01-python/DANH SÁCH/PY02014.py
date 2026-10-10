def isPrime(n) :
	for i in range(2, int(n ** 0.5) + 1) :
		if n % i == 0 : 
			return False
	return n > 1

if __name__ == "__main__" :
	n = int(input())
	a = list(map(int, input().split()))
	res = 0
	for x in a :
		d = 0
		while True :
			if x - d >= 2 and isPrime(x - d) :
				res = max(res, d)
				break
			if isPrime(x + d) :
				res = max(res, d)
				break
			d += 1
	print(res)
