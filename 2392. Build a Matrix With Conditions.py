class Solution:
    def buildMatrix(
        self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]
    ) -> List[List[int]]:
    
        def topological_sort(conditions, nums):
            inbounds = defaultdict(set)
            outbounds = {num:set() for num in nums}

            for node_from, node_to in conditions:
                outbounds[node_from].add(node_to)
                inbounds[node_to].add(node_from)

            current_level = {node for node in outbounds if node not in inbounds}

            sorted_order = []
            while current_level:
                next_level = set()
                for node in current_level:
                    sorted_order.append(node)
                    for next_node in outbounds[node]:
                        inbounds[next_node].remove(node)
                        if not inbounds[next_node]:
                            next_level.add(next_node)
                    del outbounds[node]
                current_level = next_level

            return [] if outbounds else sorted_order

        nums = {i for i in range(1, k+1)}
        row_order = topological_sort(rowConditions, nums)
        if not row_order:
            return []
        col_order = topological_sort(colConditions, nums)
        if not col_order:
            return []

        row_positions = {num: i for i, num in enumerate(row_order)}
        col_positions = {num: i for i, num in enumerate(col_order)}
        grid = [[0] * k for _ in range(k)]

        for num in range(1, k+1):
            row = row_positions.get(num, 0)
            col = col_positions.get(num, 0)
            grid[row][col] = num

        return grid
