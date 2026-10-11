from datetime import datetime

class Gamer :
    def __init__(self, id, name, time_in, time_out) :
        self.id = id
        self.name = name
        self.time_in = datetime.strptime(time_in, "%H:%M")
        self.time_out = datetime.strptime(time_out, "%H:%M")
        self.seconds = (self.time_out - self.time_in).seconds
        self.hours = self.seconds // 3600
        self.minutes = (self.seconds - self.hours * 3600) // 60

    def __str__(self) :
        return f"{self.id} {self.name} {self.hours} gio {self.minutes} phut"

if __name__ == "__main__" :
    n = int(input())
    a = []
    for i in range(n) :
        a.append(Gamer(input(), input(), input().strip(), input().strip()))
    a.sort(key= lambda x : (-x.hours, -x.minutes))
    print(*a, sep="\n")