### insert into list
class Solution:
    def countSmaller(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        
        pretendTree = []
        
        res = []
        for n in nums[::-1]:
            pos = bisect.bisect_left(pretendTree, n)
            pretendTree.insert(pos, n)
            res.append(pos)
            
        return res[::-1]
