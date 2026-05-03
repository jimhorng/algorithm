from __future__ import annotations


class SegmentTree:
    def __init__(self, n: int) -> None:
        size = 4 * (n + 1)
        self.mn = [0] * size
        self.mx = [0] * size
        self.lazy = [0] * size

    def range_add(self, node: int, left: int, right: int, ql: int, qr: int, delta: int) -> None:
        if ql <= left and right <= qr:
            self._apply(node, delta)
            return

        self._push(node)
        mid = (left + right) // 2
        if ql <= mid:
            self.range_add(node * 2, left, mid, ql, qr, delta)
        if mid < qr:
            self.range_add(node * 2 + 1, mid + 1, right, ql, qr, delta)
        self._pull(node)

    def find_first(self, node: int, left: int, right: int, target: int) -> int:
        if left == right:
            return left

        self._push(node)
        mid = (left + right) // 2
        left_child = node * 2

        if self.mn[left_child] <= target <= self.mx[left_child]:
            return self.find_first(left_child, left, mid, target)
        return self.find_first(left_child + 1, mid + 1, right, target)

    def _apply(self, node: int, delta: int) -> None:
        self.mn[node] += delta
        self.mx[node] += delta
        self.lazy[node] += delta

    def _push(self, node: int) -> None:
        delta = self.lazy[node]
        if delta == 0:
            return
        self._apply(node * 2, delta)
        self._apply(node * 2 + 1, delta)
        self.lazy[node] = 0

    def _pull(self, node: int) -> None:
        self.mn[node] = min(self.mn[node * 2], self.mn[node * 2 + 1])
        self.mx[node] = max(self.mx[node * 2], self.mx[node * 2 + 1])


class Solution:
    def longestBalanced(self, nums: list[int]) -> int:
        n = len(nums)
        tree = SegmentTree(n)
        last_seen: dict[int, int] = {}
        current = 0
        answer = 0

        for index, value in enumerate(nums, start=1):
            contribution = 1 if value % 2 else -1

            if value in last_seen:
                tree.range_add(1, 0, n, last_seen[value], n, -contribution)
                current -= contribution

            last_seen[value] = index
            tree.range_add(1, 0, n, index, n, contribution)
            current += contribution

            start_prefix = tree.find_first(1, 0, n, current)
            answer = max(answer, index - start_prefix)

        return answer


if __name__ == "__main__":
    from test_cases import run_cases

    run_cases(Solution())
