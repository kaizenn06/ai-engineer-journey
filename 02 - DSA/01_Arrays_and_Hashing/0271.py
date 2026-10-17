class Solution:

    def encode(self, strs: List[str]) -> str:
        s = ""
        for str in strs:
            s += f'{len(str)}#{str}'
        return s

    def decode(self, s: str) -> List[str]:
        words = []
        i = 0
        while i < len(s):
            j = i
            while s[j] != '#':
                j += 1
            num = int(s[i : j])
            word = s[j + 1 : j + 1 + num]
            words.append(word)
            i = j + 1 + num
        return words
