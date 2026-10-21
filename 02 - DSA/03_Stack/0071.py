class Solution:
    def simplifyPath(self, path: str) -> str:
        paths = path.split('/')
        result = []
        for p in paths:
            if p == '..':
                if result:
                    result.pop()
            elif p != '.' and p != '':
                result.append(p)
        return '/' + '/'.join(result)