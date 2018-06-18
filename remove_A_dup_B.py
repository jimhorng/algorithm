class Solution(object):
    def AB(self, s):
        size_org = len(s)
        a_count, b_count = 0, 0
        a_start = None
        for i in range(len(s)):
            if s[i] == 'B':
                b_count += 1
            elif s[i] == 'A':
                s[i] = None
                if a_start is None:
                    a_start = i
                a_count += 1
            if s[i] is not None and a_start is not None:
                s[i], s[a_start] = s[a_start], s[i]
                a_start += 1

        if b_count > a_count:
            s.extend([None] * (b_count - a_count))
        else:
            for _ in range(a_count-b_count):
                s.pop()
        # print("DEBUG: ", s, "a_start:", a_start)    

        i = size_org - a_count - 1
        j = len(s) - 1
        while i >= 0: # td
            if s[i] == 'B':
                s[i], s[j] = s[j], s[i]
                s[j-1] = 'B'
                j -= 1
            else:
                s[i], s[j] = s[j], s[i]
            j -= 1
            i -= 1
        return s

run = Solution().AB

def testcase(expected, *args):
    import time
    time_start = time.time()
    result = run(*args)
    print("{!s:<10}{!s:<50}{!s:<50}{:<10.2f}{!s:<10}".format(result == expected, expected, result, (time.time()-time_start)*1000, str(args)[:64]))
print("{:<10}{:<50}{:<50}{:<10}{:<10}".format("pass?", "expected", "result", "took(ms)", "test_case"))

testcase(['C', 'B', 'B', 'C', 'B', 'B'], ['A', 'C', 'B', 'C', 'B'])
testcase(['B', 'B', 'C'], ['A', 'B', 'A', 'C'])
