if __name__ == "__main__" : 
	n = input()
	t = len(n) // 2
	while len(n) > 1 :
		t = len(n) // 2
		sum = int(n[:t]) + int(n[t:])
		n = str(sum)
		print(sum)
