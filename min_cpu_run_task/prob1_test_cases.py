prob1_test_cases = [
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
    },
    {
        "testcase": "additional_test_1",
        # deadline=9; t0[0-5], t4 needs free<=4 but CPU1 free at 5 -> 2nd CPU;
        # 2nd CPU free at 4, end=9 ok; 3rd task s=4 needs free<=4 but both at 5,9 -> 3rd CPU
        "start_times": [0, 4, 4],
        "task_length": 5,
        "expected": 3
    },
    {
        "testcase": "additional_test_2",
        # deadline=8; dense overlap [0,1,2] then [4,5]; needs 3 CPUs
        "start_times": [0, 1, 2, 4, 5],
        "task_length": 3,
        "expected": 3
    },
    {
        "testcase": "additional_test_3",
        # tasks chain perfectly: [0-5]->[5-10]->[10-15]->[15-20], 1 CPU suffices
        "start_times": [0, 5, 10, 15],
        "task_length": 5,
        "expected": 1
    },
    {
        "testcase": "additional_test_4",
        # deadline=14; t0[0-5], t4[4-9..actual 5-10], t9 needs free<=9;
        # CPU1 free at 10 > 9 -> 2nd CPU; 2nd t9 fits on either -> 2 CPUs
        "start_times": [0, 4, 9, 9],
        "task_length": 5,
        "expected": 2
    },
]
