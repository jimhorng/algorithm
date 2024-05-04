class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        n = len(nums)

        i_empty = None
        prev_num, prev_cnt = None, 0
        for i in range(n):
            # dups to remove
            if nums[i] == prev_num and prev_cnt == 2:
                nums[i] = None
                # if cur is 1st to remove
                if i_empty is None: i_empty = i
                continue
            # new num
            if nums[i] != prev_num: prev_num, prev_cnt = nums[i], 1
            # same num
            elif nums[i] == prev_num: prev_cnt += 1
            # if has removed before
            if i_empty is not None:
                nums[i_empty], nums[i] = nums[i], nums[i_empty]
                i_empty += 1

        return i_empty if i_empty is not None else n
