class Solution:
    def minKBitFlips(self, nums: List[int], k: int) -> int:
        n = len(nums)
        flips = 0
        to_flips = deque()
        i = 0
        for i in range(n):
            while to_flips and to_flips[0] < i:
                to_flips.popleft()
            val = (nums[i] + len(to_flips)) % 2
            i_win_end = i+k-1
            if val == 0:
                if i_win_end > n-1:
                    return -1
                flips += 1
                to_flips.append(i_win_end)
        return flips
