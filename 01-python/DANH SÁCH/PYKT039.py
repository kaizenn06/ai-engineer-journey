if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = int(input())
		a = list(map(int, input().split()))
		b = list(map(int, input().split()))
		a = sorted(a)
		b = sorted(b)
		ok = True
		for i in range(n) :
			if a[i] > b[i] :
				ok = False
				break
		print("YES" if ok else "NO")
