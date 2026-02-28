"""
Problem 1: Fixed Duration, Shared Deadline
Approach: Forward greedy -- sort by start_time + min-heap (no binary search)

Algorithm
---------
Sort tasks by start_time.  Maintain a min-heap of CPU free times.
For each task with start_time s:
  f           = earliest-free CPU
  actual_start = max(f, s)   -- wait for CPU if busy, or start at s if CPU idle
  end          = actual_start + task_length

  if end <= final_deadline:  reuse this CPU (pop f, push end)
  else:                      open new CPU   (push s + task_length)

final_deadline = last_start_time + task_length  (shared deadline, prob1 semantics)

"Open new CPU" is always correct when the earliest-free CPU fails:
  every other CPU has free_time2 >= f, so actual_start2 >= actual_start,
  so end2 >= end > final_deadline.  No existing CPU can help.
  New CPU starts the task at s (task_length <= last_start_time guarantees
  s + task_length <= final_deadline, so the new CPU always succeeds).

Time Complexity : O(n log n)  -- sort + n heap pushes/pops of O(log k) each
Space Complexity: O(n)        -- heap holds at most n CPU free times
"""

import heapq


def prob1(start_times, task_length):
    if not start_times:
        return 0

    sorted_starts = sorted(start_times)
    final_deadline = sorted_starts[-1] + task_length  # shared deadline

    cpu_heap = []  # min-heap of CPU free times

    for s in sorted_starts:
        if cpu_heap:
            f = cpu_heap[0]                        # earliest-free CPU
            actual_start = max(f, s)               # wait for CPU or start now
            if actual_start + task_length <= final_deadline:
                heapq.heappop(cpu_heap)
                heapq.heappush(cpu_heap, actual_start + task_length)
                continue
        # No existing CPU can meet the deadline — open a new one
        heapq.heappush(cpu_heap, s + task_length)  # new CPU starts task at s

    return len(cpu_heap)

