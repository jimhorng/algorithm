"""
Problem 3: Fixed Duration, Per-Task Deadline
Approach: Forward greedy -- sort by start_time + min-heap

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
