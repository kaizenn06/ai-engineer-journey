class Candidates :
    def __init__(self, id, name, team) :
        self.id = f"C{id:03d}"
        self.name = name
        self.team = team

    def __str__(self) :
        return f"{self.id} {self.name} {self.team[0]} {self.team[1]}"

if __name__ == "__main__" :
    n = int(input())
    teams = {}
    for i in range(n) :
        teams[f'Team{i + 1:02d}'] = [input(), input()]
    m = int(input())
    a = []
    for i in range(m) :
        a.append(Candidates(i + 1, input(), teams[input()]))
    a.sort(key= lambda x : x.name)
    print(*a, sep= '\n')