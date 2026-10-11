if __name__ == "__main__" :
	t = int(input())
	fibo = [0] * 95
	fibo[1] = fibo[2] = 1
	for i in range(3, 93) :
		fibo[i] = fibo[i - 1] + fibo[i - 2]
	for _ in range(t) :
		a, b = map(int, input().split())
		for i in range(a, b + 1) :
			print(fibo[i], end = " ")
		print()
