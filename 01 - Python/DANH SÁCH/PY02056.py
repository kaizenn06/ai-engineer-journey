def check(n) :
	n = str(n)
	return len(n) > 1 and n == n[::-1]

if __name__ == "__main__" :
	n, m = map(int, input().split())
	a = list(list(map(int, input().split())) for _ in range(n))
	maxVal = max((a[i][j] for i in range(n) for j in range(m) if check(a[i][j])), default=-1)
	if maxVal == -1 :
		print("NOT FOUND")
	else :	
		print(maxVal)
		pos = [(i, j) for i in range(n) for j in range(m) if a[i][j] == maxVal]
		for (i, j) in pos :
			print(f"Vi tri [{i}][{j}]")
