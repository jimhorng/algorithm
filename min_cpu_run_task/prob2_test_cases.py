"""
Test cases for Problem 2: Variable Duration, Minimize End Time
"""

prob2_test_cases = [
    {
        "testcase": "varying_lengths_sequential",
        "start_times": [0, 10, 25],
        "task_lengths": [10, 15, 5],
        "expected": 1  # Can all run sequentially
    },
    {
        "testcase": "varying_lengths_overlap",
        "start_times": [0, 0, 5],
        "task_lengths": [10, 5, 3],
        "expected": 2  # Task 0 on CPU1, Task 1&2 on CPU2
    },
    {
        "testcase": "all_same_start_varying_length",
        "start_times": [0, 0, 0],
        "task_lengths": [5, 10, 3],
        "expected": 2  # longest task (10) on CPU1; shorter tasks (5,3) share CPU2
        # CPU1: [0-10]; CPU2: [0-5][5-8] -> end=10=min_possible
    },
    {
        "testcase": "short_then_long",
        "start_times": [0, 0, 10],
        "task_lengths": [5, 15, 20],
        "expected": 2  # CPU1: [0-5], [10-30]; CPU2: [0-15]
    },
    {
        "testcase": "optimal_packing",
        "start_times": [0, 5, 10, 15],
        "task_lengths": [5, 5, 5, 5],
        "expected": 1  # All fit sequentially on one CPU
    },
    {
        "testcase": "long_task_blocks",
        "start_times": [0, 1, 2],
        "task_lengths": [20, 3, 3],
        "expected": 2  # Long task blocks, short tasks share CPU
    },
    {
        "testcase": "mixed_gaps",
        "start_times": [0, 3, 6, 9],
        "task_lengths": [3, 3, 3, 3],
        "expected": 1  # back-to-back sequential: [0-3][3-6][6-9][9-12] -> end=12
    },
    # ── Counter-examples exposing greedy failures ──────────────────────────
    {
        # sol2 over-counts (GREEDY REUSE IS WRONG):
        # sol2 reuses the only CPU for (4,5) after (0,7), pushing it to end=12.
        # All remaining tasks then exceed min_possible_end=14 on that CPU -> 4 CPUs.
        # Optimal: pair (0,7)+(7,6) on CPU1, (4,5)+(8,4) on CPU2, (6,8) on CPU3.
        "testcase": "sol2_greedy_reuse_fails",
        "start_times":  [0, 4, 6, 7, 8],
        "task_lengths":  [7, 5, 8, 6, 4],
        "expected": 3
    },
    {
        # BOTH sol1 and sol2 over-count (SORT ORDER IS WRONG):
        # Sort (start,-length) puts (2,6) before (2,1).
        # Optimal needs (2,1) chained *before* (2,6) on the same CPU:
        #   CPU1: (4,8)[4-12] + (5,2)[12-14]
        #   CPU2: (2,1)[2-3]  + (2,6)[3-9] + (9,6)[9-15]
        # Neither sol tries that ordering.
        "testcase": "sort_order_fails_both_sols",
        "start_times":  [2, 2, 4, 5,  9],
        "task_lengths":  [1, 6, 8, 2,  6],
        "expected": 2
    },
]
