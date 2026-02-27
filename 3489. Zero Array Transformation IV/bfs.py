class Solution:
    def minZeroArray(self, nums: List[int], queries: List[List[int]]) -> int:
        n = len(nums)
        m = len(queries)

        def get_iq_min(i):
            num = nums[i]
            if num == 0:
                return -1
            q = deque() # (num_re, iq)
            q.append((num, 0))
            visited = {(num, 0)} # added in q
            while q:
                num_re, iq = q.popleft()
                ql, qr, qv = queries[iq]
                iq_nx = iq+1
                if ql <= i <= qr:
                    num_re_nx = num_re - qv
                    # meet
                    if num_re_nx == 0:
                        return iq
                    if not ((num_re_nx, iq_nx) in visited or iq_nx > m-1):
                        # use
                        q.append((num_re_nx, iq_nx))
                        visited.add((num_re_nx, iq_nx))
                if not ((num_re, iq_nx) in visited or iq_nx > m-1):
                    # not use
                    q.append((num_re, iq_nx))
                    visited.add((num_re, iq_nx))
            return None

        # main
        iq_min_global = -1
        for i in range(n):
            iq_min = get_iq_min(i)
            if iq_min is None:
                return -1
            iq_min_global = max(iq_min_global, iq_min)
        return iq_min_global + 1
