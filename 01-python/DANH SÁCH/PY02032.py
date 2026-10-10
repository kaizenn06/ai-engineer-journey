if __name__ == "__main__" :
	n = input()
	s = set()
	for i in range(0, len(n), 2) :
		if len(n[i:i + 2]) == 1 : continue
		s.add(n[i:i + 2])
	print(" ".join(sorted(s)))
	

	
