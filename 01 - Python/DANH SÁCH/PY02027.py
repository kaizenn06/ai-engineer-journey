if __name__ == "__main__" :
	n = int(input())
	a = []
	for _ in range(n) :
		s = input()
		num = ""
		for c in s :
			if c.isdigit() :
				num += c
			else : 
				if num :
					a.append(int(num))
					num = ""
		if num : a.append(int(num))
	a = sorted(a)
	print("\n".join(str(x) for x in a))
