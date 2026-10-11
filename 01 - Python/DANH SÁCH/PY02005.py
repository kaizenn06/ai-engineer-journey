if __name__ == "__main__" :
	n = int(input())
	a = [int(x) for x in input().split()]
	d = 0
	for i in range(len(a)) :
		for j in range(i + 1, len(a)) :
			if a[i] > a[j] :
				d += 1
	print(d)
