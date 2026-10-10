from math import factorial
if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = input()
		s = 0
		for i in range(len(n)) :
			s += factorial(int(n[i]))
		print("Yes" if s == int(n) else "No")
		
