import sys
if __name__ == "__main__" :
	a = [int(x) for x in sys.stdin.read().split()]
	s = set()
	for x in a :
		s.add(x % 42)
	print(len(s)) 
