if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n, m, k = map(int, input().split())
		a = list(map(int, input().split()))
		b = list(map(int, input().split()))
		c = list(map(int, input().split()))
		i, j, l = 0, 0, 0
		ok = False
		while i < n and j < m and l < k :
			if a[i] == b[j] == c[l] :
				print(a[i], end = " ")
				ok = True
				i += 1
				j += 1
				l += 1
			else :
				mn = min(a[i], b[j], c[l])
				if a[i] == mn : i += 1
				if b[j] == mn : j += 1
				if c[l] == mn : l += 1
		if not ok : print("NO", end = " ")
		print()
