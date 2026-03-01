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
        "testcase": "sol2_max_front_wastes_chain_for_tight_deadline_task",
        # start_times=[3,5,4,10], task_length=5, deadlines=[12,14,9,17]
        # Sol2 backward order (start DESC): T3(10,17)->T1(5,14)->T2(4,9)->T0(3,12)
        # T1 attaches to T3 chain (max_front=12, effective=12>=10 ✓), front->7.
        # T2: effective=min(9,7)=7 < 9 -> new CPU.
        # T0: effective=min(12,7)=7 < 8 -> new CPU. Returns 3.
        # Optimal (2 CPUs): c1: T2[4,9]->T3[10,15]; c2: T0[3,8]->T1[5,10] ... wait
        # c1: T2[4,9] T3[10,15]; c2: T0[3,8] T1[8,13] (T1 starts at max(8,5)=8 ✓)
        "start_times": [3, 5, 4, 10],
        "task_length": 5,
        "deadlines": [12, 14, 9, 17],
        "expected": 2
    },
    # ── Known failure for ALL sols (strategic idling required) ──────────────
    {
        "testcase": "strategic_idling_all_sols_fail",
        # T0(s=1,d=6), T1(s=4,d=14), T2(s=6,d=9), L=3
        # EDF order on 1 CPU: T0[1,4] -> idle [4,6] -> T2[6,9] -> T1[9,12]<=14 ✓
        # All sols schedule T1 at t=4 (it's available) instead of idling for T2,
        # forcing T2 onto a new CPU. Optimal=1 but all sols return 2.
        "start_times": [1, 4, 6],
        "task_length": 3,
        "deadlines": [6, 14, 9],
        "expected": 1
    },
    # ── Known failure for sol2 + sol3 (different-release EDF ordering) ──────
    {
        "testcase": "different_release_edf_sol2_sol3_fail",
        # T0(s=5,d=18), T1(s=6,d=18), T2(s=7,d=14), T3(s=8,d=20), T4(s=9,d=21), L=5
        # T2 has tightest latest_start=9. With k=2, must schedule T2 before T0/T1
        # even though T0 and T1 are released earlier.
        # sol3 pre-sorts by (release, ls): (5,13),(6,13),(7,9),(8,15),(9,16)
        #   k=2: CPU1 takes T0[5,10], CPU2 takes T1[6,11], then T2 sees both CPUs
        #   free at 10/11 > ls=9 -> declared infeasible -> returns 3. Wrong.
        # sol1 (forward greedy) happens to get 2 by not reusing early for T2.
        # Correct: CPU1: T0[5,10]->T3[10,15]; CPU2: T2[7,12]->T1[12,17]<=18 ✓;
        #   T4[17,22]<=21? No. Try: CPU1: T2[7,12]->T4[12,17]; CPU2: T0[5,10]->T3[10,15];
        #   T1[15,20]<=18? No. CPU1: T0[5,10]->T2[10,15]<=14? No (10>ls=9).
        #   CPU1: T1[6,11]; CPU2: T2[7,12]->... wait T2 ls=9, must start by 9.
        #   CPU1: T2[7,12]? 12>14? No 12<=14 ✓. T0[5,10]->T3[10,15]; T1[6,11]->T4[11,16]
        #   Check: CPU1: T0[5,10] T3[10,15]; CPU2: T1[6,11] T4[11,16]<=21 ✓ T2?
        #   Need 3rd CPU for T2 unless... CPU2: T2[7,12] T? -- only 2 tasks per CPU.
        #   Optimal 2-CPU: CPU1: T0[5,10]->T3[10,15]; CPU2: T2[7,12]->T1[12,17]<=18 ✓
        #     T4: max(15,9)=15, 15+5=20<=21 ✓ on CPU1 after T3. CPU1: T0 T3 T4.
        #     CPU1: T0[5,10]->T3[10,15]->T4[15,20]<=21 ✓  CPU2: T2[7,12]->T1[12,17]<=18 ✓
        "start_times": [5, 6, 7, 8, 9],
        "task_length": 5,
        "deadlines": [18, 18, 14, 20, 21],
        "expected": 2
    }
]
