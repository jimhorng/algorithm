"""
1) binary search for max stay mins still pass
"""

"""
You are situated in the top-left cell, (0, 0), and you want to travel to the safehouse at the bottom-right cell, (m - 1, n - 1)
grid[i][j] value is 0, 1, 2
if grid[i][j] = 0, you can move
if grid[i][j] = 1, fire, spread 1 cell in 4 direction every mins
if grid[i][j] = 2, blocked 

<algo>
- binary search for max_mins, with conditions for `can_stay()`
- `can_stay(mins)`: spread all fire(1) cell `mins` times, using bfs, mark grid as 1
    and for each following mins till m*n mins, human move use bfs + visited to move
    see if can reach cell (m - 1, n - 1), return True if can, False if not
"""
from collections import deque
from typing import List
import math

class Solution:
    def maximumMinutes(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])

        def can_stay(mins):
            # Create a copy of the grid to track fire spread
            fire_grid = [row[:] for row in grid]
            
            # Find initial fire cells
            fire_queue = deque()
            for i in range(m):
                for j in range(n):
                    if grid[i][j] == 1:
                        fire_queue.append((i, j, 0))  # (row, col, time)
            
            # Spread fire for `mins` minutes
            fire_time = {}
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            
            while fire_queue:
                r, c, t = fire_queue.popleft()
                if (r, c) in fire_time:
                    continue
                fire_time[(r, c)] = t
                
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in fire_time:
                        if grid[nr][nc] == 0:  # Can spread to empty cell
                            fire_queue.append((nr, nc, t + 1))
            
            # Now simulate human movement starting at time `mins`
            if (0, 0) in fire_time and fire_time[(0, 0)] < mins:
                return False  # Starting cell already on fire
            
            human_queue = deque([(0, 0, mins)])  # (row, col, time)
            visited = {(0, 0)}
            
            while human_queue:
                r, c, t = human_queue.popleft()
                
                # Check if we reached the destination
                if r == m - 1 and c == n - 1:
                    return True
                
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in visited:
                        if grid[nr][nc] == 0:  # Empty cell
                            # Check if fire hasn't reached this cell yet or reaches at the same time
                            if (nr, nc) not in fire_time or fire_time[(nr, nc)] > t + 1:
                                visited.add((nr, nc))
                                human_queue.append((nr, nc, t + 1))
                            # Special case: if this is the destination, allow arriving at same time as fire
                            elif (nr, nc) == (m - 1, n - 1) and fire_time[(nr, nc)] >= t + 1:
                                visited.add((nr, nc))
                                human_queue.append((nr, nc, t + 1))
            
            return False

        # Check if we can reach destination even without waiting
        if not can_stay(0):
            return -1
        
        max_mins = 0
        # normal
        l, r = 0, m * n
        while l <= r:
            mid = math.floor((l+r)/2)
            if can_stay(mid):
                max_mins = max(max_mins, mid)
                l = mid + 1
            else:
                r = mid - 1
        if max_mins == m * n:
            return 10**9
        return max_mins


# Test case
if __name__ == "__main__":
    sol = Solution()
    
    # Test case: grid = [[0,0,0,0],[0,1,2,0],[0,2,0,0]]
    # Expected: -1
    grid = [[0,0,0,0],[0,1,2,0],[0,2,0,0]]
    result = sol.maximumMinutes(grid)
    print(f"Grid: {grid}")
    print(f"Result: {result}, Expected: -1")
    assert result == -1, f"Test failed! Expected -1, got {result}"
    print("Test passed!")
