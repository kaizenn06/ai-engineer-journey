if __name__ == "__main__" :
	n = int(input())
	a = list(input().split() for _ in range(n))
	res = []
	i = 0
	while i < n :
		if len(a[i]) == 6 :
			res.append(1)
			while i < n and len(a[i]) == 6 :
				i += 2
		elif len(a[i]) == 7 :
			res.append(2)
			i += 4
		else : i += 1
	print(len(res))
	for x in res :
		print(x)
