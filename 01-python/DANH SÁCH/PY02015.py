if __name__ == "__main__" :
	while True :
		a = list(map(int, input().split()))
		if all(x == 0 for x in a) : 
			break
		d = 0
		while len(set(a)) != 1 :
			b = [0] * 4
			for i in range(4) :
				b[i] = abs(a[i] - a[(i + 1) % 4])
			a = b
			d += 1
		print(d)
