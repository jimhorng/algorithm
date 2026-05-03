from __future__ import annotations


TEST_CASES = [
    ([2, 5, 4, 3], 4),
    ([3, 2, 2, 5, 4], 5),
    ([1, 2, 3, 2], 3),
    ([2], 0),
    ([2, 4, 6], 0),
    ([1, 3, 5], 0),
    ([2, 1, 2, 1], 4),
    ([2, 2, 1, 3], 3),
    ([4, 1, 4, 2, 3, 3], 6),
]


def run_cases(solution) -> None:
    for index, (nums, expected) in enumerate(TEST_CASES, start=1):
        actual = solution.longestBalanced(nums)
        assert actual == expected, (
            f"Case {index} failed: nums={nums!r}, "
            f"expected={expected!r}, got={actual!r}"
        )

    print(f"Passed {len(TEST_CASES)} test cases.")
