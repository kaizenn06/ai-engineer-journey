if __name__ == "__main__" :
	n, m = map(int, input().split())
	a = list(map(int, input().split()))
	b = list(map(int, input().split()))
	print("YES" if set(a) == set(b) else "NO")
