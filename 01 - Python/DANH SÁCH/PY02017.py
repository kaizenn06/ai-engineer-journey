if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = int(input())
		a = list(map(int, input().split()))
		mp = {}
		for x in a :
			mp[x] = mp.get(x, 0) + 1
		for x in mp :
			if mp[x] % 2 == 1:
				print(x)
				break
