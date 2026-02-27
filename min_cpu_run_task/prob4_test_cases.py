"""
Test cases for Problem 4: Variable Duration, Per-Task Deadline

Each task i must finish at or before deadlines[i].
Valid start window for task i: [start_times[i], deadlines[i] - task_lengths[i]]
If start_times[i] + task_lengths[i] > deadlines[i], the task is infeasible -> return -1.
Most general variant - interval graph coloring with variable-length jobs.
"""

prob4_test_cases = [
    {
        "testcase": "sequential_exact_fit",
        "start_times": [0, 10, 17],
        "task_lengths": [10, 7, 5],
        "deadlines": [10, 17, 22],  # each task pinned to exactly one start
        "expected": 1  # CPU1: task0[0-10], task1[10-17], task2[17-22]
    },
    {
        "testcase": "impossible_narrow_window",
        "start_times": [5],
        "task_lengths": [3],
        "deadlines": [7],  # 5+3=8 > 7, no valid window
        "expected": -1
    },
    {
        "testcase": "all_overlap_same_deadline",
        "start_times": [0, 0, 0],
        "task_lengths": [5, 3, 7],
        "deadlines": [7, 7, 7],
        # task0 window [0,2]; task1 window [0,4]; task2 window [0,0]
        # all windows overlap at t=0, max simultaneous = 3
        "expected": 3
    },
    {
        "testcase": "flexible_deadlines_two_cpus",
        "start_times": [0, 0, 5],
        "task_lengths": [10, 5, 3],
        "deadlines": [10, 10, 10],
        # CPU1: task0[0-10]; CPU2: task1[0-5], task2[5-8]
        "expected": 2
    },
    {
        "testcase": "tight_windows_overlap",
        "start_times": [0, 3, 6],
        "task_lengths": [5, 5, 5],
        "deadlines": [8, 11, 14],
        # task0 window [0,3]; task1 window [3,6]; task2 window [6,9]
        # max overlap of execution intervals = 2 (task0&task1 can overlap)
        # CPU1: task0[0-5], task2[6-11]; CPU2: task1[3-8]
        "expected": 2
    },
    {
        "testcase": "one_task_no_window",
        "start_times": [0, 0, 5],
        "task_lengths": [10, 5, 3],
        "deadlines": [10, 10, 7],  # task2: 5+3=8 > 7
        "expected": -1
    },
    {
        "testcase": "varied_lengths_sequential",
        "start_times": [0, 0, 0],
        "task_lengths": [2, 3, 5],
        "deadlines": [2, 5, 10],
        # task0 pinned [0-2]; task1 window [0,2]; task2 window [0,5]
        # CPU1: task0[0-2], task1[2-5], task2[5-10]
        "expected": 1
    },
    {
        "testcase": "generous_windows_one_cpu",
        "start_times": [0, 2, 5],
        "task_lengths": [3, 4, 6],
        "deadlines": [20, 20, 20],
        # CPU1: task0[0-3], task1[3-7], task2[7-13] - all fit sequentially
        "expected": 1
    },
    {
        "testcase": "complex_overlap_three_cpus",
        "start_times": [0, 0, 0, 5],
        "task_lengths": [10, 8, 6, 3],
        "deadlines": [10, 8, 6, 8],
        # task0 window [0,0]; task1 window [0,0]; task2 window [0,0]; task3 window [5,5]
        # tasks 0,1,2 all must start at 0 -> 3 CPUs
        # task3 window [5,5] fits on CPU2 or CPU3 after their tasks finish
        "expected": 3
    }
]
