if __name__ == "__main__" :
	n, m = map(int, input().split())
	a = list(map(int, input().split()))
	b = list(map(int, input().split()))
	print(" ".join([str(x) for x in sorted(set(a) & set(b))]))
	print(" ".join([str(x) for x in sorted(set(a) - set(b))]))
	print(" ".join([str(x) for x in sorted(set(b) - set(a))]))
