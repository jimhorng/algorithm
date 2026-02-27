"""
Test cases for Problem 3: Fixed Duration, Per-Task Deadline

Each task i must finish at or before deadlines[i].
Valid start window for task i: [start_times[i], deadlines[i] - task_length]
If start_times[i] + task_length > deadlines[i], the task is infeasible -> return -1.
Reduces to interval graph coloring: min CPUs = max overlap (clique size).
"""

prob3_test_cases = [
    {
        "testcase": "sequential_exact_fit",
        "start_times": [0, 5, 10],
        "task_length": 5,
        "deadlines": [5, 10, 15],  # window[i] = [start, start], pinned exactly
        "expected": 1  # CPU1: task0[0-5], task1[5-10], task2[10-15]
    },
    {
        "testcase": "all_tight_same_deadline",
        "start_times": [0, 0, 0],
        "task_length": 5,
        "deadlines": [5, 5, 5],  # all must run at [0-5], windows fully overlap
        "expected": 3
    },
    {
        "testcase": "mixed_deadlines_sequential",
        "start_times": [0, 0, 0],
        "task_length": 5,
        "deadlines": [5, 10, 15],
        # task0 pinned at [0-5]; task1 can start in [0,5]; task2 can start in [0,10]
        # CPU1: task0[0-5], task1[5-10], task2[10-15]
        "expected": 1
    },
    {
        "testcase": "deadline_forces_parallel",
        "start_times": [0, 0, 0],
        "task_length": 5,
        "deadlines": [5, 5, 10],
        # task0 and task1 both pinned at [0-5], need 2 CPUs for them
        # task2 window [0,5] fits on a CPU after time 5
        "expected": 2
    },
    {
        "testcase": "impossible_narrow_window",
        "start_times": [10],
        "task_length": 5,
        "deadlines": [14],  # 10+5=15 > 14, no valid start exists
        "expected": -1
    },
    {
        "testcase": "large_gap_feasible",
        "start_times": [0, 0, 0, 10000],
        "task_length": 5,
        "deadlines": [15, 15, 15, 10005],
        # first 3 run sequentially [0-5],[5-10],[10-15]; last at [10000-10005]
        "expected": 1
    },
    {
        "testcase": "one_task_impossible",
        "start_times": [0, 0, 5],
        "task_length": 5,
        "deadlines": [10, 10, 9],  # task2: 5+5=10 > 9
        "expected": -1
    },
    {
        "testcase": "overlap_forces_two",
        "start_times": [0, 3, 8],
        "task_length": 5,
        "deadlines": [8, 11, 13],
        # task0 window [0,3]; task1 window [3,6]; task2 window [8,8]
        # task0 and task1 windows overlap -> max simultaneous overlap = 2
        "expected": 2
    },
    # ── Known failures for sol1 (EDF) and sol2 (deadline-DESC) ──────────────
    {
        "testcase": "edf_fails_looser_deadline_must_run_first",
        # T1(s=5,d=8) is pinned at [5,8]. T0(s=0,d=9) must run at [0,3] to
        # leave the CPU free for T1. EDF schedules T1 first (tighter deadline),
        # forcing T0 to start at 8 => end=11 > 9. Both deadline-based sorts fail.
        # Optimal: T0[0,3] -> gap -> T1[5,8] on 1 CPU.
        "start_times": [0, 5],
        "task_length": 3,
        "deadlines": [9, 8],
        "expected": 1
    },
    {
        "testcase": "edf_fails_three_task_pinned_middle",
        # T1(s=6,d=9) is pinned at [6,9]. T0(s=3,d=10) must run at [3,6]
        # (before T1) even though T0's deadline is later. EDF schedules T1 first,
        # leaving T0 no room before its deadline of 10. T2 chains after T1.
        # Optimal: T0[3,6] -> T1[6,9] -> T2[9,12] on 1 CPU.
        "start_times": [3, 6, 9],
        "task_length": 3,
        "deadlines": [10, 9, 13],
        "expected": 1
    },
    # ── Known failure for sol1 only (greedy reuse) ──────────────────────────
    {
        "testcase": "sol1_greedy_reuse_blocks_tight_deadline_tasks",
        # T0,T1 (flexible, d=20) both arrive at 0. Sol1 reuses the same CPU for
        # T1 after T0, making that CPU free at 10. T2,T3 (tight, d=11) then
        # arrive at 6 but need a CPU free at <=6. None available -> 2 new CPUs.
        # Optimal: put T0 and T1 on separate CPUs so each is free at 5,
        # allowing T2[6,11] and T3[6,11] to reuse them. -> 2 CPUs total.
        "start_times": [0, 0, 6, 6],
        "task_length": 5,
        "deadlines": [20, 20, 11, 11],
        "expected": 2
    },
    # ── Known failure for sol2 only (max-front greedy wastes high-front chains) ──
    {
        "testcase": "sol2_max_front_wastes_chain_for_same_start_tasks",
        # T1(3,13) has the highest deadline among same-start tasks.
        # Sol2 attaches T1 to the T3(10,17) chain (max_front=12), dropping
        # that chain's front to 7. T0 and T2 (also start=3) then need
        # effective=min(12|10, 7)=7 >= 3+5=8, which fails -> 2 new CPUs.
        # Optimal: CPU1: T2[3,8]->T3[10,15]; CPU2: T0[3,8]->T1[8,13].
        # T0 and T1 have the same start so they can be chained sequentially,
        # freeing the high-front chain for T2+T3 instead.
        "start_times": [3, 3, 3, 10],
        "task_length": 5,
        "deadlines": [12, 13, 10, 17],
        "expected": 2
    }
]
