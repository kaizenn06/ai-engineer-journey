def isPrime(n) :
	for i in range(2, int(n ** 0.5) + 1) :
		if n % i == 0 : 
			return False
	return n > 1

if __name__ == "__main__" :
	n = int(input())
	a = list(map(int, input().split()))
	d = [0] * 1005
	b = []
	for x in a :
		if d[x] : continue
		d[x] += 1
		b.append(x)
	sum1 = 0
	idx = -1
	for i in range(len(b)) :
		sum1 += b[i]
		if not isPrime(sum1) : continue
		sum2 = 0
		for j in range(i + 1, len(b)) :
			sum2 += b[j]
		if isPrime(sum2) : 
			idx = i
			break
	print("NOT FOUND" if idx == -1 else idx)
	

	
