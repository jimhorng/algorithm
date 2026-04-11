"""
You are situated in the top-left cell, start (0, 0), and you want to travel to the safehouse at the bottom-right cell end (m - 1, n - 1)
grid[i][j] value is 0, 1, 2
if grid[i][j] = 0, you can move
if grid[i][j] = 1, fire, spread 1 cell in 4 direction every mins
if grid[i][j] = 2, blocked 

<algo>
- spread all fire(1) cell till fill all cells, using bfs, mark grid as k mins
- human move from start cell, use dijkstra to move toward end cell,
    - diff = fire mins - human mins as edge weight
    - max path weight as goal
"""
from collections import deque
from typing import List, Dict, Tuple
import heapq


class Solution:
    def maximumMinutes(self, grid: List[List[int]]) -> int:
        self.m, self.n = len(grid), len(grid[0])
        self.grid = grid
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Calculate fire spread times
        fire_time = self._calculate_fire_spread()
        
        # Check if start position is valid
        if not self._is_start_valid(fire_time):
            return -1
        
        # Calculate human travel times
        human_time = self._calculate_human_times()
        
        # Check if destination is reachable
        if not self._is_destination_reachable(human_time):
            return -1
        
        # Find maximum wait time using Dijkstra
        return self._find_max_wait_time(fire_time, human_time)
    
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
    
    def _calculate_human_times(self) -> Dict[Tuple[int, int], int]:
        """Calculate shortest time for human to reach each cell using BFS."""
        human_time = {}
        queue = deque([(0, 0, 0)])
        human_time[(0, 0)] = 0
        
        while queue:
            r, c, t = queue.popleft()
            
            for dr, dc in self.directions:
                nr, nc = r + dr, c + dc
                if self._is_valid_cell(nr, nc) and (nr, nc) not in human_time:
                    if self.grid[nr][nc] == 0:
                        human_time[(nr, nc)] = t + 1
                        queue.append((nr, nc, t + 1))
        
        return human_time
    
    def _find_max_wait_time(self, fire_time: Dict, human_time: Dict) -> int:
        """Find maximum wait time at start using Dijkstra to maximize bottleneck."""
        pq = [(-float('inf'), 0, 0)]  # (-max_wait, row, col)
        visited = {}
        
        while pq:
            neg_wait, r, c = heapq.heappop(pq)
            wait = -neg_wait
            
            if (r, c) in visited:
                continue
            visited[(r, c)] = wait
            
            # Reached destination
            if self._is_destination(r, c):
                return 10**9 if wait == float('inf') else wait
            
            # Explore neighbors
            for dr, dc in self.directions:
                nr, nc = r + dr, c + dc
                if self._is_valid_cell(nr, nc) and (nr, nc) not in visited:
                    if (nr, nc) in human_time:
                        new_wait = self._calculate_wait_time(nr, nc, wait, fire_time, human_time)
                        if new_wait is not None:
                            heapq.heappush(pq, (-new_wait, nr, nc))
        
        return -1
    
    def _calculate_wait_time(self, r: int, c: int, current_wait: float, 
                            fire_time: Dict, human_time: Dict) -> int:
        """Calculate the maximum wait time for a given cell."""
        if (r, c) not in fire_time:
            # Fire never reaches this cell
            return current_wait
        
        margin = fire_time[(r, c)] - human_time[(r, c)]
        
        # Destination: can arrive at same time as fire
        if self._is_destination(r, c):
            if margin >= 0:
                return margin if current_wait == float('inf') else min(current_wait, margin)
            return None
        
        # Intermediate cell: must arrive before fire
        if margin > 0:
            return (margin - 1) if current_wait == float('inf') else min(current_wait, margin - 1)
        
        return None
    
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
    print("Test 2 passed!")
