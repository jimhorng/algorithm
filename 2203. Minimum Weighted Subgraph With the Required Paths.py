from typing import List
import heapq
from collections import defaultdict

class Solution:
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
        # Build adjacency list
        graph = defaultdict(list)
        for u, v, w in edges:
            graph[u].append((v, w))
        
        # Track minimum distance to reach each node with each source combination
        # dist[node][has_src1][has_src2] = min_distance
        # Boolean indices: False=0, True=1
        dist = [[[float('inf')] * 2 for _ in range(2)] for _ in range(n)]
        
        pq = []
        # Start from src1 - mark as containing src1
        start_src1 = (src1 == src1)  # True
        start_src2_from_src1 = (src1 == src2)  # True only if src1 == src2
        dist[src1][start_src1][start_src2_from_src1] = 0
        heapq.heappush(pq, (0, src1, start_src1, start_src2_from_src1))
        
        # Start from src2 - mark as containing src2
        start_src1_from_src2 = (src2 == src1)  # True only if src1 == src2
        start_src2 = (src2 == src2)  # True
        dist[src2][start_src1_from_src2][start_src2] = 0
        heapq.heappush(pq, (0, src2, start_src1_from_src2, start_src2))
        
        while pq:
            d, node, has_src1, has_src2 = heapq.heappop(pq)
            
            # Skip if we've found a better path
            if d > dist[node][has_src1][has_src2]:
                continue
            
            # Explore neighbors
            for neighbor, weight in graph[node]:
                new_dist = d + weight
                # Update flags if neighbor is a source
                neighbor_has_src1 = has_src1 or (neighbor == src1)
                neighbor_has_src2 = has_src2 or (neighbor == src2)
                
                if new_dist < dist[neighbor][neighbor_has_src1][neighbor_has_src2]:
                    dist[neighbor][neighbor_has_src1][neighbor_has_src2] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor, neighbor_has_src1, neighbor_has_src2))
                    
                    # Try to merge: if exactly one source, check for complementary path
                    if neighbor_has_src1 != neighbor_has_src2:  # XOR: (T,F) or (F,T)
                        comp_src1 = not neighbor_has_src1
                        comp_src2 = not neighbor_has_src2
                        
                        if dist[neighbor][comp_src1][comp_src2] < float('inf'):
                            merged_dist = new_dist + dist[neighbor][comp_src1][comp_src2]
                            if merged_dist < dist[neighbor][True][True]:
                                dist[neighbor][True][True] = merged_dist
                                heapq.heappush(pq, (merged_dist, neighbor, True, True))
        
        # Return minimum distance to dest with both sources
        result = dist[dest][True][True]
        return result if result < float('inf') else -1


# Test cases
if __name__ == "__main__":
    sol = Solution()
    tests = [
        # (n, edges, src1, src2, dest, expected, description)
        (4, [[0, 2, 2], [1, 2, 3], [2, 3, 1]], 0, 1, 3, 6, "Basic case"),
        (6, [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]], 0, 1, 5, 9, "LeetCode example"),
        (3, [[0, 1, 1]], 0, 1, 2, -1, "No path exists"),
        (3, [[0, 1, 2], [1, 2, 3]], 0, 0, 2, 5, "src1 == src2"),
        (3, [[0, 2, 1], [1, 2, 2]], 0, 1, 2, 3, "Source is destination"),
        (8, [[4,7,24],[1,3,30],[4,0,31],[1,2,31],[1,5,18],[1,6,19],[4,6,25],[5,6,32],[0,6,50]], 4, 1, 6, 44, "")
    ]
    
    for i, (n, edges, src1, src2, dest, expected, desc) in enumerate(tests, 1):
        result = sol.minimumWeight(n, edges, src1, src2, dest)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"Test {i} {status}: {desc} (got {result}, expected {expected})")
       