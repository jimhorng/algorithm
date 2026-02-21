test_cases = [
    {
        "testcase": "example1_large_gap",
        "start_times": [0, 0, 0, 10000],
        "task_length": 5,
        "expected": 1
    },
    {
        "testcase": "example2_all_same_start",
        "start_times": [0, 0, 0],
        "task_length": 5,
        "expected": 3
    },
    {
        "testcase": "single_task",
        "start_times": [0],
        "task_length": 10,
        "expected": 1
    },
    {
        "testcase": "two_tasks_overlap",
        "start_times": [0, 3],
        "task_length": 5,
        "expected": 2
    },
    {
        "testcase": "two_tasks_no_overlap",
        "start_times": [0, 10],
        "task_length": 5,
        "expected": 1
    },
    {
        "testcase": "multiple_overlapping",
        "start_times": [0, 1, 2, 3, 4],
        "task_length": 10,
        "expected": 5
    },
    {
        "testcase": "partial_overlap",
        "start_times": [0, 5, 10],
        "task_length": 7,
        "expected": 2
    },
    {
        "testcase": "fifty_tasks_grouped_overlaps",
        "start_times": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                        10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                        15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
                        20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
        "task_length": 6,
        "expected": 20
    }
]
