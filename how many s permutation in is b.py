# xrange = range

class Solution(object):
    def run(self, s, b):
        import copy
        import collections
        s_hash = {}
        for c in s:
            s_hash[c] = s_hash.get(c, 0) + 1

        l = 0
        r = l + len(s) - 1
        s_tmp = copy.copy(s_hash)
        s_cur = collections.deque()
        for i in range(l, r+1):
            s_cur.append(b[i])
            if s_tmp.get(b[i]):
                s_tmp[b[i]] -= 1
                if s_tmp[b[i]] == 0:
                    del s_tmp[b[i]]
        results = []
        if len(s_tmp) == 0:
            results.append("".join(s_cur))
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
            s_cur.append(b[r])
            s_cur.popleft()
            if len(s_tmp) == 0:
                results.append("".join(s_cur))
            

        return results

run = Solution().run

def testcase(expected, *args):
    import time
    time_start = time.time()
    result = run(*args)
    print("{:<10}{:<10}{:<10}{:<10.2f}{:<10}".format(str(result == expected), str(expected), str(result), (time.time()-time_start)*1000, str(args)))
print("{:<10}{:<10}{:<10}{:<10}{:<10}".format("pass?", "expected", "result", "took(ms)", "test_case"))

testcase(["cbab"], "abbc", "cbabadcbbabbcbabaabccbabc")
