class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n
        prefix = 1
        for i in range(n) :
            result[i] = prefix 
            prefix *= nums[i]
        #pre : 1 1 2 8
        suffix = 1
        for i in range(n - 1, -1, -1) :
            result[i] *= suffix
            suffix *= nums[i]
        #suf : 1 6 24 48
        return result
