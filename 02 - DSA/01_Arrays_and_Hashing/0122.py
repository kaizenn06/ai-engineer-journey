class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maximum = 0
        for i in range(len(prices) - 1):
            maximum += max(0, prices[i + 1] - prices[i])
        return maximum