"""
Problem 3 — Solution 3: Forward + Binary Search
=================================================

Algorithm
---------
Use a prob1-style pattern for per-task deadlines:
1) Pre-check impossibility: if start_i + L > deadline_i for any task -> -1.
2) Sort tasks by (release_time, latest_start) -- encodes EDF within each
   release group statically, eliminating the need for a dynamic available-heap.
3) Binary search on CPU count k in [1, n].
4) For fixed k, run a forward feasibility simulation.

Forward feasibility simulation
------------------------------
Maintain a deque of CPU next-free times (always sorted, see invariant below).

At each step, popleft the earliest-free CPU time `t`:
- If t < next task's release time, fast-forward t to that release time.
- Check if t > latest_start for the next task -> infeasible.
- Assign: append t + task_length to the back of the deque.

Deque invariant (why deque works instead of a heap):
  All tasks have the same length L.  After each assignment, t + L is pushed.
  The spread of values in the deque never exceeds L:
    new value = t + L >= all existing values (t was the minimum, each existing
    value is at most t + L from the previous round).  So appending to the back
    always maintains sorted order, and popleft always gives the minimum.

Time Complexity : O(n log n) -- sorting once + O(log n) x O(n) simulation
                               simulation is O(n) deque ops (no heap overhead)
Space Complexity: O(n)
"""

from __future__ import annotations
from collections import deque


def _feasible_with_k(tasks: list[tuple[int, int]], task_length: int, num_cpus: int) -> bool:
    """
    Check whether all tasks can be scheduled on `num_cpus` CPUs.

    tasks: list of (release_time, latest_start), sorted by (release_time, latest_start).
    machines: deque of CPU next-free times, maintained in sorted order.
    """
    machines = deque([0] * num_cpus)

    for release, latest_start in tasks:
        current_time = machines.popleft()

        # fast-forward idle CPU to task's release time
        if current_time < release:
            current_time = release

        if current_time > latest_start:
            return False

        machines.append(current_time + task_length)

    return True


def prob3(start_times: list[int], task_length: int, deadlines: list[int]) -> int:
    """
    Return the minimum number of CPUs required so that each task finishes
    by its own deadline, or -1 if impossible.
    """
    n = len(start_times)
    if n == 0:
        return 0

    tasks: list[tuple[int, int]] = []
    for start_time, deadline in zip(start_times, deadlines):
        latest_start = deadline - task_length
        if latest_start < start_time:
            return -1
        tasks.append((start_time, latest_start))

    # Sort by (release_time, latest_start): EDF within same release group
    tasks.sort()

    left, right = 1, n
    while left < right:
        mid = (left + right) // 2
        if _feasible_with_k(tasks, task_length, mid):
            right = mid
        else:
            left = mid + 1

    return left
