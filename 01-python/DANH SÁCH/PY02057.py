if __name__ == "__main__" :
	n, m = map(int, input().split())
	a = list(list(map(int, input().split())) for _ in range(n))
	minVal = min(min(row) for row in a)
	maxVal = max(max(row) for row in a)
	luckyVal = maxVal - minVal
	pos = [(i, j) for i in range(n) for j in range(m) if a[i][j] == luckyVal]
	if not pos :
		print("NOT FOUND")
	else :	
		print(luckyVal)
		for (i, j) in pos :
			print(f"Vi tri [{i}][{j}]")
