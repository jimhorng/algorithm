class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        def find_cycle_path(node, parent, path, visited, graph):
            # if cycle found
            if node in visited:
                result = {tuple(sorted([path[-1],node]))}
                for i in range(len(path)-2, -1, -1):
                    result.add(tuple(sorted([path[i], path[i+1]])))
                    if path[i] == node: break
                return result
            visited.add(node)
            path.append(node)
            for node_nx in graph[node]:
                if node_nx == parent:
                    continue
                result = find_cycle_path(node_nx, node, path, visited, graph)
                if result:
                    return result
            path.pop()
            return None

        graph = defaultdict(list)
        for v1, v2 in edges:
            graph[v1].append(v2)
            graph[v2].append(v1)

        cycle_path = find_cycle_path(1, None, [], set(), graph)
        # print(f"cycle_path:{cycle_path}")
        for edge in reversed(edges):
            if tuple(edge) in cycle_path:
                return edge
