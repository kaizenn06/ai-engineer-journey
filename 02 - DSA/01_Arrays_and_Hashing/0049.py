class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = {}
        for str in strs:
            key = ''.join(sorted(str))
            if key not in groups:
                groups[key] = []
            groups[key].append(str)
        return list(groups.values())