from math import sqrt
prime = [0] * 1000005
if __name__ == "__main__" :
	n, x = map(int, input().split()) 
	for i in range(2, 1000001) :
		prime[i] = i
	for i in range(2, int(sqrt(1000001))) :
		if prime[i] :
			for j in range(i*i, 1000001, i) :
				prime[j] = 0
	a = []
	a.append(0)
	for i in range(2, 1000001) :
		if len(a) == 1005 : break
		if prime[i] : 
			a.append(i)
	for i in range(n + 1) :
		x += a[i]
		print(x, end = " ")
