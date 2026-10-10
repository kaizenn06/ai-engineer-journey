from math import gcd
if __name__ == "__main__" :
	n = int(input())
	a = list(map(float, input().split()))
	mx, mn = 0, 10
	for i in range(n) :
		if a[i] < mn : mn = a[i]
		if a[i] > mx : mx = a[i]
	sum = 0
	d = 0
	for i in range(n) :
		if a[i] == mx : continue
		if a[i] == mn : continue
		sum += a[i]
		d += 1
	print(f"{(sum / d):.2f}")
	
