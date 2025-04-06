class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prod = 1
        r = -1
        result = 0
        for l in range(n): # 1
            # prev win ended, start new
            if r < l:
                r = l
                prod = nums[r]
            # move win right as much
            while r+1 <= n-1 and prod * nums[r+1] < k:
                r += 1
                prod = prod * nums[r]
            if prod < k: result += (r-l+1)
            # move l
            prod = prod / nums[l]
        return result
