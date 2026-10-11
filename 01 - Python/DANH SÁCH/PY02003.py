from bisect import bisect_left
a = []
limit = 10**18
def sinh() :
	x = 1
	while x <= limit :
		y = x
		while y <= limit :
			z = y
			while z <= limit : 
				a.append(z)
				z *=5
			y *= 3
		x *= 2
	a.sort()

if __name__ == "__main__" :
	sinh()
	t = int(input())
	for _ in range(t) :
		n = int(input())
		idx = bisect_left(a, n)
		if idx < len(a) and a[idx] == n :
			print(idx + 1)
		else :
			print("Not in sequence")
