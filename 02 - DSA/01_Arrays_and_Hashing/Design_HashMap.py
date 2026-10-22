class MyHashMap:

    def __init__(self):
        self.HashMap = []

    def put(self, key: int, value: int) -> None:
        if key not in self.HashMap:
            self.HashMap.append([key, value])

    def get(self, key: int) -> int:
        if key in self.HashMap:
            return self.HashMap[self.HashMap.index[key]]

    def remove(self, key: int) -> None:
        if key in self.HashMap:
            self.HashMap.remove(self.HashMap[self.HashMap.index[key]])