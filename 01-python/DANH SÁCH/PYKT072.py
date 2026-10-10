if __name__ == "__main__" :
	n = int(input())
	a = list(input() for _ in range(n))
	taget = a[0]
	ans = float('inf')
	for i in range(len(taget)) :
		allOK = True
		d = 0
		for j in range(n) :
			s = a[j]
			ok = False
			for k in range(len(s)) :
				if s == taget :
					ok = True
					d += k
					break
				s = s[1:] + s[0]
			if not ok : 
				allOK = False
				break
		if allOK :
			ans = min(ans, d)
		taget = taget[1:] + taget[0]
	print(-1 if ans == float('inf') else ans)
		
