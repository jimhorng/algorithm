"""
Problem 3: Fixed Duration, Per-Task Deadline
Approach: Forward greedy -- sort by start_time + min-heap

Key differences from prob1_sol1
---------------------------------
prob1 has a SHARED final deadline (last_start + task_length); prob3 has a
PER-TASK deadline.  This changes two things:

1. Sort order: sort by (start_time, deadline) -- same as prob1.
   Although each task has its own deadline, sorting by start_time ensures we
   process tasks in chronological order.  Sorting by deadline (EDF) instead
   breaks the greedy: a looser-deadline task may need an earlier clock slot
   so that a tighter-deadline task can be pinned to a later slot.

   Counter-example for EDF:
     starts=[0,5], L=3, deadlines=[9,8]
     T1 (deadline=8) scheduled first: occupies [5,8].
     T0 (deadline=9) must start at 8 -> ends 11 > 9.  EDF says 2 CPUs.
     With start_time sort: T0 -> [0,3], T1 -> [5,8].  1 CPU suffices.

2. No binary search needed: the feasibility check per task is self-contained.
   For each task we ask "can the earliest-free CPU meet THIS task's deadline?"
   If not, a new CPU is opened for this task.
   (Proof: if earliest-free CPU at time f gives actual_start = max(f, s) with
   actual_start + L > deadline, then every other CPU is free at f2 >= f, so
   actual_start2 >= actual_start > deadline - L.  No existing CPU helps.)

3. Feasibility pre-check: if start_times[i] + task_length > deadlines[i] for
   any task, it is impossible regardless of CPU count.

Known Failure — greedy reuse is not globally optimal
------------------------------------------------------
The greedy "always reuse the earliest-free CPU if it fits" can over-allocate.
Reusing an early-free CPU for a flexible task advances its free time, making
it unavailable for future tight-deadline tasks that needed that early slot.

  Counter-example: starts=[0,0,6,6], L=5, deadlines=[20,20,11,11]
    T0(s=0,d=20): new CPU A, free=5.
    T1(s=0,d=20): f=5, actual=5, 10<=20 → REUSE A, free=10.  <-- greedy reuse
    T2(s=6,d=11): f=10, actual=10, 15>11 → new CPU B.
    T3(s=6,d=11): f=10, 15>11 → new CPU C.  sol1 returns 3.

  Optimal (don't reuse A for T1; open new CPU B instead):
    CPU A free=5: T2 → actual=max(5,6)=6, 11<=11 ✓
    CPU B free=5: T3 → actual=6, 11<=11 ✓   → 2 CPUs.

This is the same class of flaw as prob2_sol1/sol2: greedy reuse sacrifices
future flexibility.  A correct solution requires backtracking or min-cost flow.

Algorithm
---------
1. Pre-check: any start + L > deadline → return -1.
2. Sort tasks by (start_time, deadline).
3. Min-heap of CPU free times (initially empty).
4. For each task (start, L, deadline):
     f = heap minimum (earliest-free CPU)
     actual_start = max(f, start)
     if actual_start + L <= deadline:
         pop f, push actual_start + L     # reuse CPU
     else:
         push start + L                   # new CPU, task starts at earliest
5. Return len(heap).

Time Complexity : O(n log n)  -- sort + n heap operations of O(log k) each
Space Complexity: O(n)        -- heap holds one entry per CPU
"""

import heapq


def prob3(start_times, task_length, deadlines):
    if not start_times:
        return 0

    # Pre-check: any task whose window is empty is infeasible
    if any(s + task_length > d for s, d in zip(start_times, deadlines)):
        return -1

    # Sort by (start_time, deadline) -- chronological order
    tasks = sorted(zip(start_times, deadlines), key=lambda x: (x[0], x[1]))

    cpu_heap = []  # min-heap of CPU free times

    for start, deadline in tasks:
        if cpu_heap:
            f = cpu_heap[0]                    # earliest-free CPU
            actual_start = max(f, start)
            if actual_start + task_length <= deadline:
                heapq.heappop(cpu_heap)
                heapq.heappush(cpu_heap, actual_start + task_length)
                continue
        # No existing CPU can meet the deadline -- open a new one
        heapq.heappush(cpu_heap, start + task_length)

    return len(cpu_heap)
