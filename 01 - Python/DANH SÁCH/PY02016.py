if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = int(input())
		a = list(map(int, input().split()))
		mp = {}
		m = 0
		for x in a :
			mp[x] = mp.get(x, 0) + 1
			m = max(m, mp[x])
		if m <= n // 2 :
			print("NO")
			continue
		for x in mp :
			if mp[x] == m :
				print(x)
				break
