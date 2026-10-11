def isPrime(n) :
	for i in range(2, int(n ** 1/2) + 1) :
		if n % i == 0 : 
			return False
	return n > 1
if __name__ == "__main__" :
	n = int(input())
	a = list(map(int, input().split()))
	mp = {}
	for i in range(n) :
		if isPrime(a[i]) :
			mp[a[i]] = mp.get(a[i], 0) + 1
	for x in mp :
		print(x, mp.get(x))
