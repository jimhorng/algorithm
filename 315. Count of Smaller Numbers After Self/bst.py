class Solution:
    def countSmaller(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        class Node:
            def __init__(self, val):
                self.val = val
                self.smallers = 0
                self.dups = 1
                self.left = None
                self.right = None
        if not nums:
            return []
        result = [0]
        bst = Node(nums[-1])
        for num in reversed(nums[:-1]):
            cur = bst
            smallers = 0
            while True:
                if num > cur.val:
                    smallers += cur.smallers + cur.dups
                    if cur.right:
                        cur = cur.right
                    else:
                        cur.right = Node(num)
                        break
                elif num == cur.val:
                    cur.dups += 1
                    smallers += cur.smallers
                    break
                elif num < cur.val:
                    cur.smallers += 1
                    if cur.left:
                        cur = cur.left
                    else:
                        cur.left = Node(num)
                        break
                    
            result.append(smallers)
        return list(reversed(result))
