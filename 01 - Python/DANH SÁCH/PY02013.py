if __name__ == "__main__" :
	while True :
		n = int(input())
		if n == 0 : break
		s = set()
		while n != 1 :
			if n % 2 == 0 : 
				n = n // 2
			else : n = n * 3 + 1
			s.add(n)
		print(len(s) + 1)
