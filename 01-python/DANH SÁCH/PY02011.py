if __name__ == "__main__" :
	n = int(input())
	a = list(map(int, input().split()))
	res = float("inf")
	ans = 0
	for x in a :
		t = sum(abs(i - x) for i in a)
		if t < res :
			res = t
			ans = x
	print(res, ans)

		
