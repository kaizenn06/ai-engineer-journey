if __name__ == "__main__" :
	n, k = map(int, input().split())
	a = list(map(int, input().split()))
	a = sorted(a)
	d = 1
	for i in range(1, n) :
		if a[i] - a[i - 1] > k :
			d +=1
	print(d)
