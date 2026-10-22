class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def merge_sort(nums, l, r):
            if l >= r:
                return
            m = (l + r) // 2
            merge_sort(nums, l, m)
            merge_sort(nums, m + 1, r)
            merge(nums, l, m, r)
        
        def merge(nums, l, m, r):
            left = nums[l: m + 1]
            right = nums[m + 1: r + 1]
            i, j = 0, 0
            k = l
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    nums[k] = left[i]
                    i += 1
                else:
                    nums[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                nums[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                nums[k] = right[j]
                j += 1
                k += 1
        merge_sort(nums, 0, len(nums) - 1)
        return nums