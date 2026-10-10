if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = int(input())
		a = [int(x) for x in input().split()]
		b = [int(x) for x in input().split()]
		a.sort()
		b.sort()
		ok = True
		for i in range(n) :
			if a[i] > b[i] :
				ok = False
				break
		print("YES" if ok else "NO")
