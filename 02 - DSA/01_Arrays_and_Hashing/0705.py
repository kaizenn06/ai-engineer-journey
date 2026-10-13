class MyHashSet:

    def __init__(self):
        self.HashSet = []

    def add(self, key: int) -> None:
        if key not in self.HashSet :
            self.HashSet.append(key)

    def remove(self, key: int) -> None:
        if key in self.HashSet :
            self.HashSet.remove(key)

    def contains(self, key: int) -> bool:
        return key in self.HashSet