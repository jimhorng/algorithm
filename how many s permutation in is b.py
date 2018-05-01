# xrange = range

class Solution(object):
    def findAnagrams1_1(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: List[int]
        """
        p_hash = {}
        for c in p:
            p_hash[c] = p_hash.get(c, 0) + 1
        l = 0
        r = 0
        results = []
        while r <= len(s) - 1:
            p_hash[s[r]] = p_hash.get(s[r], 0) - 1
            if p_hash[s[r]] == 0:
                del p_hash[s[r]]
            if len(p_hash) == 0:
                results.append(l)
            r += 1
            if r - l >= len(p):
                p_hash[s[l]] = p_hash.get(s[l], 0) + 1
                if p_hash[s[l]] == 0:
                    del p_hash[s[l]]
                l += 1

        return results
    
    
    def run(self, b, s):
        import copy
        s_hash = {}
        for c in s:
            s_hash[c] = s_hash.get(c, 0) + 1

        l = 0
        r = l + len(s) - 1
        s_tmp = copy.copy(s_hash)
        for i in range(l, r+1):
            if s_tmp.get(b[i]):
                s_tmp[b[i]] -= 1
                if s_tmp[b[i]] == 0:
                    del s_tmp[b[i]]
        results = []
        if len(s_tmp) == 0:
            results.append(l)
        while r <= len(b) - 2:
            if b[l] in s_hash and s_tmp.get(b[l], 0) != s_hash.get(b[l]):
                s_tmp[b[l]] = s_tmp.get(b[l], 0) + 1
                if s_tmp[b[l]] == 0:
                    del s_tmp[b[l]]
            l += 1
            r += 1
            if b[r] in s_hash:
                s_tmp[b[r]] = s_tmp.get(b[r], 0) - 1
                if s_tmp[b[r]] == 0:
                    del s_tmp[b[r]]
            if len(s_tmp) == 0:
                results.append(l)
            

        return results

run = Solution().findAnagrams1_1

def testcase(expected, *args):
    import time
    time_start = time.time()
    result = run(*args)
    print("{:<10}{:<10}{:<10}{:<10.2f}{:<10}".format(str(result == expected), str(expected), str(result), (time.time()-time_start)*1000, str(args)))
print("{:<10}{:<10}{:<10}{:<10}{:<10}".format("pass?", "expected", "result", "took(ms)", "test_case"))

testcase([0, 6, 9, 11, 12, 20, 21], "cbabadcbbabbcbabaabccbabc", "abbc")
testcase([0, 6], "cbaebabacd", "abc")
