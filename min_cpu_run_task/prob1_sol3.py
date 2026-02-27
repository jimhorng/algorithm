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

Difference from sol1
--------------------
sol1 wraps the simulation in a binary search, testing k = 1..n CPUs each time
and stopping as soon as k CPUs are sufficient.  This sol3 runs ONE pass with
no pre-set limit, always opening a new CPU the moment the earliest-free one
can't make the deadline.  The single-pass logic is equivalent to the inner
_simulate() of sol1, but without the binary search overhead.

However, sol1's binary-search framing means the simulation uses EXACTLY k CPUs
(a fixed-size deque), so it never speculatively opens CPUs — it either reuses
one of the k available slots or declares k insufficient.  Sol3 has no such cap
and can open CPUs greedily even when a smarter assignment would avoid it.

Known Failure -- greedy reuse over-advances CPU free times
----------------------------------------------------------
When a task fits on the earliest-free CPU (end <= final_deadline), the greedy
always reuses it.  This advances that CPU's free time, which can push it past
the start of later tight-deadline tasks that needed an early slot.

  Counter-example: start_times = [0]*10 + [5]*10 + ... + [20]*10, task_length=6
    final_deadline = 26.
    No CPU can chain a s=15 task (ends ≥ 21) then a s=20 task (needs free ≤ 20).
    So the 10 s=15 and 10 s=20 tasks require 20 separate CPUs.
    Optimal: 10 CPUs each run g1→g2→g3→g5 (free at 18 ≤ 20) → handle all 50
    tasks on 20 CPUs.
    Greedy deeply chains early tasks, advancing every CPU's free time past 20
    before the s=20 batch arrives → opens 10 extra CPUs → returns 30.

  Root cause: same class of flaw as prob2_sol1/sol2 and prob3_sol1 — greedy
  reuse sacrifices future flexibility for tight-deadline tasks.
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

