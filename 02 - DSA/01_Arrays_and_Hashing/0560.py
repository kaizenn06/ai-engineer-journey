class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        prefix_count = {0: 1}
        prefix = 0
        count = 0
        for num in nums :
            prefix += num
            count += prefix_count.get(prefix - k, 0)
            prefix_count[prefix] = prefix_count.get(prefix, 0) + 1
        return count 
