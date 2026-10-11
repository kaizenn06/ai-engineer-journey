if __name__ == "__main__" :
	n = input()
	s = set()
	a = []
	for i in range(0, len(n) - 1, 2) :
		x = n[i:i+2]
		if x not in s :
			s.add(x)
			a.append(x)
	print(" ".join(a))
	

	
