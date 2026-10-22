class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        longest = 0
        nums = set(nums)
        for num in nums:
            if num - 1 not in nums:
                d = 0
                while num + d in nums:
                    d += 1
                longest = max(longest, d)
        return longest