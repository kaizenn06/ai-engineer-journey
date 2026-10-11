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
	t = int(input())
	for _ in range(t) :
		sieve()
		n = int(input())
		for i in range(11, n) :
			j = int(str(i)[::-1])
			if j > n : continue
			if prime[i] and prime[j] and i != j :
				prime[i] = 0
				print(i, j, end = " ")
		print()
