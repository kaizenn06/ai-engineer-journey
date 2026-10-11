if __name__ == "__main__" :
	n, m = map(int, input().split())
	a = list(map(int, input().split()))
	d = [0] * 10
	for x in a :
		d[x] += 1
	max1, max2 = -1, -1
	for i in range(n) :
		max1 = max(max1, d[a[i]])
		if d[a[i]] < max1 :
			max2 = max(max2, d[a[i]])
	for i in range(10) :
		if d[i] == max2 :
			print(i)
			break
	if max2 == -1 : print("NONE")
	

	
