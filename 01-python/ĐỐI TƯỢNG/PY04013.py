class Rain :
    def __init__(self, id, name, start_time, end_time, rainfall) :
        self.id = f"T{id:02d}"
        self.name = name
        self.time = self.minutes(end_time) - self.minutes(start_time)
        self.rainfall = rainfall

    def minutes(self, time) :
        h, m = map(int, time.split(':'))
        return h * 60 + m

    def __str__(self) :
        return f'{self.id} {self.name} {self.rainfall / (self.time / 60) :.2f}'

if __name__ == '__main__' :
    n = int(input())
    ds = {}
    i = 1
    for _ in range(n) :
        name = input()
        start_time = input()
        end_time = input()
        rainfall = float(input())
        if name not in ds : 
            ds[name] = Rain(i, name, start_time, end_time, rainfall)
            i += 1
        else :
            ds[name].time += ds[name].minutes(end_time) - ds[name].minutes(start_time)
            ds[name].rainfall +=  rainfall
    for name in ds :
        print(ds[name])