class Solution:
    def minJumps(self, arr: List[int]) -> int:
        n = len(arr)
        dest = n-1

        # {1:{0,1,2,3}}
        val_idx = defaultdict(set) # {val:set(idx)}
        for idx, val in enumerate(arr):
            val_idx[val].add(idx)

        queue = deque() # (idx, step)
        queue.append((0, 0))
        visited = {0} # {0}
        val_idx[arr[0]].remove(0) # {1:{1,2,3}}
        while queue: # [(1,1), (2,1), (3,1)]
            idx, step = queue.popleft() # 0, 0
            if idx == dest:
                return step
            for idx_nx in [idx+1, idx-1] + list(val_idx[arr[idx]]):
                if idx_nx not in visited and (0 <= idx_nx <= n-1): # 3
                    queue.append((idx_nx, step+1)) # [(1,1), (2,1), (3,1)]
                    visited.add(idx_nx) # {0,1,2,3}
            val_idx[arr[idx]] = set()
        return None
