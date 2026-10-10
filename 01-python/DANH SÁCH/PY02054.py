if __name__ == "__main__" :
	n, m = map(int, input().split())
	a = list(list(map(int, input().split())) for _ in range(n))
	d = abs(n - m)
	if n > m :
		for i in range(n) :
			if (i + 1) % 2 == 1 and d > 0 :
				d -= 1
				continue
			print(" ".join(map(str, a[i])))
	elif n < m :
		delete = []
		for i in range(m) :
			if (i + 1) % 2 == 0 and len(delete) < d :
				delete.append(i)
		for i in range(n) :
			row = [str(a[i][j]) for j in range(m) if j not in delete]
			print(" ".join(row))
	else :
		for i in range(n) :
			print(" ".join(map(str, a[i])))
