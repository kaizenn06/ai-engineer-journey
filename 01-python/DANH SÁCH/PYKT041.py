import math
if __name__ == "__main__" :
	n = int(input())
	a = list(list(input()) for _ in range(n))
	ans = 0
	for i in range(n) :
		d = 0
		for j in range(n) :
			if a[i][j] == 'C' :
				d += 1
		ans += math.comb(d, 2)
		d = 0
		for j in range(n) :
			if a[j][i] == 'C' :
				d += 1
		ans += math.comb(d, 2)
	print(ans)
