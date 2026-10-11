from math import sqrt
prime = [0] * 1000005
def sieve() :
	for i in range(2, 1000001) :
		prime[i] = i
	for i in range(2, int(sqrt(1000001))) :
		if prime[i] :
			for j in range(i * i, 1000001, i) :
				prime[j] = 0
		
if __name__ == "__main__" :
	sieve()
	t = int(input())
	for _ in range(t) :
		n = int(input())
		d = 0
		for i in range(2, n - 6) :
			if (prime[i] and prime[i + 2] and prime[i + 6]):
				d += 1
			if (prime[i] and prime[i + 4] and prime[i + 6]):
				d += 1
		print(d)
