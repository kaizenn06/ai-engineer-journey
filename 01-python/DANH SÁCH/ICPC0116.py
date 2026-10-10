if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = input()
		print("YES" if n[0] == n[len(n) - 1] else "NO")
		
