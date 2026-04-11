"""
You are situated in the top-left cell, start (0, 0), and you want to travel to the safehouse at the bottom-right cell end (m - 1, n - 1)
grid[i][j] value is 0, 1, 2
if grid[i][j] = 0, you can move
if grid[i][j] = 1, fire, spread 1 cell in 4 direction every mins
if grid[i][j] = 2, blocked 

<algo>

"""
"""
You are situated in the top-left cell, start (0, 0), and you want to travel to the safehouse at the bottom-right cell end (m - 1, n - 1)
grid[i][j] value is 0, 1, 2
if grid[i][j] = 0, you can move
if grid[i][j] = 1, fire, spread 1 cell in 4 direction every mins
if grid[i][j] = 2, blocked 

<algo>
- spread all fire(1) cell till fill all cells, using bfs, mark grid as k mins
"""
from collections import deque
from typing import List, Dict, Tuple
import heapq
import sys


class Solution:

    MAX = sys.maxsize

    def maximumMinutes(self, grid: List[List[int]]) -> int:
        self.m, self.n = len(grid), len(grid[0])
        self.grid = grid
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Calculate fire spread times
        fire_time = self._calculate_fire_spread()
        
        # Calculate human travel times
        diff_time = self._calculate_human_times(fire_time)
        
        # invalid
        if (self.m-1, self.n-1) not in diff_time:
            return -1
        # wait forever
        result = diff_time[(self.m-1, self.n-1)]
        if result >= self.MAX - 1:  # Handle MAX or MAX-1 from intermediate cells
            return 10**9
        # max wait
        return result - 1
    
    def _calculate_fire_spread(self) -> Dict[Tuple[int, int], int]:
        """Calculate when fire reaches each cell using BFS."""
        fire_time = {}
        queue = deque()
        
        # Initialize with all fire cells
        for i in range(self.m):
            for j in range(self.n):
                if self.grid[i][j] == 1:
                    queue.append((i, j, 0))
                    fire_time[(i, j)] = 0
        
        # BFS to spread fire
        while queue:
            r, c, t = queue.popleft()
            
            for dr, dc in self.directions:
                nr, nc = r + dr, c + dc
                if self._is_valid_cell(nr, nc) and (nr, nc) not in fire_time:
                    if self.grid[nr][nc] == 0:
                        fire_time[(nr, nc)] = t + 1
                        queue.append((nr, nc, t + 1))
        
        return fire_time
    
    def _calculate_human_times(self, fire_time) -> Dict[Tuple[int, int], int]:
        """
        Calculate max wait time for human to reach each cell using BFS.
        diff_time[(r, c)]: max minutes we can wait at start before moving to this cell
        """
        queue = deque([(0, 0, 0, self.MAX)]) # (r, c, time, d_prev)
        diff_time = {}

        while queue:
            r, c, t, d_prev = queue.popleft()
            
            diff_time_cur = ((fire_time[(r, c)] - t)
                              if (r, c) in fire_time else self.MAX)
            
            diff_time_min = min(diff_time_cur, d_prev)
            # For destination, can arrive at same time as fire (diff_time_cur)
            if (r, c) == (self.m - 1, self.n - 1) and diff_time_cur >= 0:
                diff_time[(r, c)] = diff_time_min
                continue      
            # Skip if already processed with better or equal margin
            if diff_time_min <= 0 or ((r, c) in diff_time and diff_time_min <= diff_time[(r, c)]):
                continue
            diff_time[(r, c)] = diff_time_min
            
            nt = t + 1
            for dr, dc in self.directions:
                nr, nc = r + dr, c + dc
                if self._is_valid_cell(nr, nc) and self.grid[nr][nc] == 0:
                    queue.append((nr, nc, nt, diff_time[(r, c)]))

        return diff_time

    def _is_valid_cell(self, r: int, c: int) -> bool:
        """Check if cell coordinates are within grid bounds."""
        return 0 <= r < self.m and 0 <= c < self.n
    
    def _is_destination(self, r: int, c: int) -> bool:
        """Check if cell is the destination."""
        return r == self.m - 1 and c == self.n - 1
    
    def _is_start_valid(self, fire_time: Dict) -> bool:
        """Check if start position is valid (not blocked or on fire)."""
        return self.grid[0][0] != 2 and ((0, 0) not in fire_time or fire_time[(0, 0)] > 0)
    
    def _is_destination_reachable(self, human_time: Dict) -> bool:
        """Check if destination is reachable by human."""
        return (self.m - 1, self.n - 1) in human_time


# Test case
if __name__ == "__main__":
    sol = Solution()
    
    # Test case 1: grid = [[0,0,0,0],[0,1,2,0],[0,2,0,0]]
    # Expected: -1
    grid = [[0,0,0,0],[0,1,2,0],[0,2,0,0]]
    result = sol.maximumMinutes(grid)
    print(f"Test 1 - Grid: {grid}")
    print(f"Result: {result}, Expected: -1")
    assert result == -1, f"Test 1 failed! Expected -1, got {result}"
    print("Test 1 passed!\n")
    
    # Test case 2: grid = [[0,2,0,0,0,0,0],[0,0,0,2,2,1,0],[0,2,0,0,1,2,0],[0,0,2,2,2,0,2],[0,0,0,0,0,0,0]]
    # Expected: 3
    grid = [[0,2,0,0,0,0,0],[0,0,0,2,2,1,0],[0,2,0,0,1,2,0],[0,0,2,2,2,0,2],[0,0,0,0,0,0,0]]
    result = sol.maximumMinutes(grid)
    print(f"Test 2 - Grid: {grid}")
    print(f"Result: {result}, Expected: 3")
    assert result == 3, f"Test 2 failed! Expected 3, got {result}"
    print("Test 2 passed!\n")
    
    # Test case 3: grid = [[0,2,0,0,1],[0,2,0,2,2],[0,2,0,0,0],[0,0,2,2,0],[0,0,0,0,0]]
    # Expected: 0
    grid = [[0,2,0,0,1],[0,2,0,2,2],[0,2,0,0,0],[0,0,2,2,0],[0,0,0,0,0]]
    result = sol.maximumMinutes(grid)
    print(f"Test 3 - Grid: {grid}")
    print(f"Result: {result}, Expected: 0")
    assert result == 0, f"Test 3 failed! Expected 0, got {result}"
    print("Test 3 passed!\n")
    
    # Test case 4: grid = [[0,0,0],[2,2,0],[1,2,0]]
    # Expected: 1000000000
    grid = [[0,0,0],[2,2,0],[1,2,0]]
    result = sol.maximumMinutes(grid)
    print(f"Test 4 - Grid: {grid}")
    print(f"Result: {result}, Expected: 1000000000")
    assert result == 1000000000, f"Test 4 failed! Expected 1000000000, got {result}"
    print("Test 4 passed!")
