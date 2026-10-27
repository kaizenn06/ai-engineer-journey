class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        l, r = max(weights), sum(weights)
        while l < r:
            used_day = 1
            current_weight = 0
            m = (l + r) // 2
            for weight in weights:
                if current_weight + weight > m:
                    used_day += 1
                    current_weight = 0
                current_weight += weight
            if used_day <= days:
                r = m
            else:
                l = m + 1
        return l