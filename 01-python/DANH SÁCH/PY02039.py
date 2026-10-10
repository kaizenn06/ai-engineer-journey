if __name__ == "__main__" :
	n = int(input())
	a = list(list(map(int, input().split())) for _ in range(n))
	k = int(input())
	sum1, sum2 = 0, 0
	for i in range(n) :
		for j in range(n) :
			if j > i :
				sum1 += a[i][j]
			if j < i :
				sum2 += a[i][j]
	print("YES" if abs(sum1 - sum2) <= k else "NO")
	print(abs(sum1 - sum2))
