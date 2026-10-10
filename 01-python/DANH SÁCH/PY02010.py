if __name__ == "__main__" :
	while True :
		n = int(input())
		if n == 0 : break
		mn = 10 ** 101
		mx = -1
		for _ in range(n) :
			x = int(input())
			mn = min(mn, x)
			mx = max(mx, x)
		if mn == mx : 
			print("BANG NHAU")
			continue
		print(mn, mx)
		
