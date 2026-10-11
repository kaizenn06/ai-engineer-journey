if __name__ == "__main__" :
	n = input()
	m = {}
	for i in range(0, len(n) - 1, 2) :
		x = n[i:i+2]
		m[x] = m.get(x, 0) + 1
	for x in m :
		print(x, m[x])
	

	
