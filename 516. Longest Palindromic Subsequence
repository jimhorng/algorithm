class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        n = len(s)

        @cache
        def dfs(left_end, right_start):
            if left_end < 0 or right_start > n-1: return 0

            if s[left_end] == s[right_start]:
                return dfs(left_end-1, right_start+1) + 2
            elif s[left_end] != s[right_start]:
                return max(
                    dfs(left_end-1, right_start),
                    dfs(left_end, right_start+1),
                    dfs(left_end-1, right_start+1),
                )

        result = 0
        for i in range(n):
            # contains s[i] as mid
            result = max(result, dfs(i-1, i+1) + 1)
            # not contains s[i]
            result = max(result, dfs(i, i+1))

        return result
