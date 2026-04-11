from typing import List
import heapq
from collections import defaultdict

class Solution:
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
        SRC1, SRC2, SRC12 = 0, 1, 2
        
        # Build adjacency list
        graph = defaultdict(list)
        for u, v, w in edges:
            graph[u].append((v, w))
        
        dist = {} # (node,src_type):dist
        
        pq = [] # (dist, node, src_type)
        heapq.heappush(pq, (0, src1, SRC1))
        heapq.heappush(pq, (0, src2, SRC2))
        
        while pq:
            print(f"pq:{pq}, dist:{dist}")
            d, node, src_type = heapq.heappop(pq)

            if (node, src_type) in dist and d >= dist[(node, src_type)]:
                continue
            
            if (node, src_type) == (dest, SRC12):
                return d
            
            dist[(node, src_type)] = d

            # Explore neighbors
            for neighbor, weight in graph[node]:
                new_dist = d + weight
                new_dist_s1s2 = None
                if src_type == SRC1 and (neighbor, SRC2) in dist:
                    new_dist_s1s2 = new_dist + dist[(neighbor, SRC2)]
                elif src_type == SRC2 and (neighbor, SRC1) in dist:
                    new_dist_s1s2 = new_dist + dist[(neighbor, SRC1)]
                if src_type == SRC12:
                    heapq.heappush(pq, (new_dist, neighbor, SRC12))
                else:
                    if new_dist_s1s2 is not None:
                        heapq.heappush(pq, (new_dist_s1s2, neighbor, SRC12))
                        if new_dist < new_dist_s1s2:
                            heapq.heappush(pq, (new_dist, neighbor, src_type))
                    else:
                        heapq.heappush(pq, (new_dist, neighbor, src_type))
        
        return -1


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
       