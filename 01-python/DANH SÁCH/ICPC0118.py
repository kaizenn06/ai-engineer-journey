if __name__ == "__main__" :
	t = int(input())
	name = [
		"Ma Ket", "Bao Binh", "Song Ngu", "Bach Duong",
		"Kim Nguu", "Song Tu", "Cu Giai", "Su Tu",
		"Xu Nu", "Thien Binh", "Thien Yet", "Nhan Ma", "Ma Ket"
	]
	last = [19, 18, 20, 19, 20, 20, 22, 22, 22, 22, 22, 21]
	for _ in range(t) :
		day, month = map(int, input().split())
		if day > last[month - 1] :
			print(name[month])
		else :
			print(name[month - 1])
		
