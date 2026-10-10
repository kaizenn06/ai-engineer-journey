if __name__ == "__main__" :
	n = int(input())
	a = list(list(map(int, input().split())) for _ in range(n))
	k = int(input())
	sum1, sum2 = 0, 0
	for i in range(n) :
		for j in range(n) :
			if i > j :
				sum1 += a[i][j]
			elif i < j :
				sum2 += a[i][j]
	print("YES" if abs(sum1 - sum2) < k else "NO")
	print(abs(sum1 - sum2))
