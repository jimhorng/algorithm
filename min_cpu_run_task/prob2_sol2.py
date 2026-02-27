"""
Problem 2: Variable Duration, Minimize End Time
Approach: Direct greedy with min-heap -- no binary search needed

Key idea:
  Process tasks sorted by (start_time, -task_length).
  Maintain a min-heap of CPU "available at" times.

  For each task (start, length):
    1. Peek at the earliest-available CPU (heap min).
    2. actual_start = max(start, cpu_available)
       end_time    = actual_start + length
    3. If end_time <= min_possible_end:
         Reuse this CPU -- pop it and push end_time.
    4. Else:
         No existing CPU can accommodate this task without exceeding the
         deadline. Add a new CPU: push start + length (task starts at its
         earliest nominal time on a fresh CPU).

Correctness of "new CPU" branch: The earliest-available CPU gives the
smallest possible actual_start. If even that CPU causes end > min_possible_end,
no existing CPU can do better -- a new CPU is necessary.  ✓

Known limitation 1 -- greedy reuse is suboptimal (sol2-specific):
  Reusing the earliest CPU when it "fits" can block it for tasks that ONLY
  fit on an early-ending CPU, while the current task could use a fresh CPU.

  Counter-example:
    start_times=[0,4,6,7,8], task_lengths=[7,5,8,6,4]  -> expected 3, returns 4
    Sort: (0,7),(4,5),(6,8),(7,6),(8,4). min_possible_end=14.
    Step 2 reuses the only CPU for (4,5) after (0,7), pushing it to end=12.
    All later tasks then need new CPUs (end always > 14 on that CPU). Total: 4.
    Optimal: CPU1=(0,7)+(7,6), CPU2=(4,5)+(8,4), CPU3=(6,8). 3 CPUs.
    Sol1 (binary search) handles this correctly.

Known limitation 2 -- sort order is a heuristic (shared with sol1):
  Counter-example:
    start_times=[2,2,4,5,9], task_lengths=[1,6,8,2,6]  -> expected 2, returns 3
    Optimal needs short task (2,1) chained before long (2,6) on same CPU,
    but sort puts (2,6) first. Neither sol finds the 2-CPU schedule.

Sort order: (start_time, -task_length) for the same reason as sol1:
longer tasks are harder to delay, so assign them while CPUs are free.

Time Complexity: O(n log n)  -- one pass, each step is O(log k) heap op
Space Complexity: O(k)        -- heap holds one entry per CPU
"""

import heapq


def prob2(start_times, task_lengths):
    if not start_times:
        return 0

    sorted_tasks = sorted(
        zip(start_times, task_lengths),
        key=lambda x: (x[0], -x[1])
    )

    min_possible_end = max(s + l for s, l in sorted_tasks)

    cpu_times = []  # min-heap of CPU available times

    for start, length in sorted_tasks:
        if cpu_times:
            earliest_available = cpu_times[0]       # peek min (no pop yet)
            actual_start = max(start, earliest_available)
            end_time = actual_start + length

            if end_time <= min_possible_end:
                heapq.heappop(cpu_times)             # consume this CPU slot
                heapq.heappush(cpu_times, end_time)
                continue

        # No existing CPU works (or heap is empty): allocate a new CPU.
        # Task runs from its earliest nominal start on a fresh CPU.
        heapq.heappush(cpu_times, start + length)

    return len(cpu_times)
