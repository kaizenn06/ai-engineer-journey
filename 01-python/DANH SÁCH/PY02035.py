if __name__ == "__main__" :
	n = input()
	k = int(input())
	m = {}
	for i in range(0, len(n) - 1, 2) :
		x = n[i:i+2]
		m[x] = m.get(x, 0) + 1
	m = dict(sorted(m.items(), key=lambda x : int(x[0])))
	ok = False
	for x in m :
		if m[x] < k : continue
		print(x, m[x])
		ok = True
	if not ok : print("NOT FOUND")
	

	
