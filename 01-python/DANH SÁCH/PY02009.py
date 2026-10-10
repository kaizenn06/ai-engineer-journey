if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = int(input())
		a = []
		d = [0] * 1005
		mx = 0
		for _ in range(n) :
			x = int(input())
			a.append(x)
			d[x] += 1
			mx = max(mx, d[x])
		for i in range(1001) :
			if d[i] == mx :
				print(i)
				break
		
