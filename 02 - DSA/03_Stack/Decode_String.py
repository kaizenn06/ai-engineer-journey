class Solution:
    def decodeString(self, s: str) -> str:
        result = []
        for c in s:
            if c == ']':
                res = ''
                while result and result[-1] != '[':
                    res = result.pop() + res
                result.pop()
                n = ''
                while result and result[-1].isdigit():
                    n = result.pop() + n
                res = res * int(n)
                result.append(res)
            else:
                result.append(c)
        return ''.join(result)