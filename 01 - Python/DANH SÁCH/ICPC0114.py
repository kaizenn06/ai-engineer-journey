from math import sqrt
def isPrime(n) :
	for i in range(2, int(sqrt(n)) + 1) :
		if n % i == 0 :
			return False
	return True

def check(n) :
	sum = 0
	for i in range(len(n)) :
		if n[i] != '2' and n[i] != '3' and n[i] != '5' and n[i] != '7' :
			return False
		sum += int(n[i])
	return isPrime(sum)

if __name__ == "__main__" :
	t = int(input())
	for _ in range(t) :
		n = int(input())
		rev = int(str(n)[::-1])
		if isPrime(n) and isPrime(rev) and check(str(n)) :
			print("Yes")
		else : print("No")
