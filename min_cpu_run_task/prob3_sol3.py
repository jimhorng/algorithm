"""
Problem 3 — Solution 3: Forward + Binary Search
=================================================

Approach
--------
Use a prob1-style pattern for per-task deadlines:
1) Pre-check impossibility: if start_i + L > deadline_i for any task -> -1.
2) Binary search on CPU count k in [1, n].
3) For fixed k, run a forward feasibility simulation.

Forward feasibility simulation
------------------------------
Maintain:
- `machines`: min-heap of CPU next-free times.
- `available`: min-heap of released jobs ordered by latest_start
   where latest_start = deadline - L.

At each step, pick the earliest-free machine time `t`.
- If no job is available and future jobs exist, idle this machine to the next
  release time.
- Push all jobs released by time `t` into `available`.
- Schedule the available job with smallest latest_start.
- If `t > latest_start`, schedule is infeasible for this k.

If all jobs are scheduled, k is feasible.
"""

from __future__ import annotations

import heapq


def _feasible_with_k(tasks: list[tuple[int, int]], task_length: int, num_cpus: int) -> bool:
    """
    Check whether all tasks can be scheduled on `num_cpus` CPUs.

    tasks: list of (release_time, latest_start), sorted by release_time.
    """
    n = len(tasks)

    machines = [0] * num_cpus
    heapq.heapify(machines)

    available: list[tuple[int, int]] = []  # (latest_start, release_time)
    idx = 0

    while True:
        if idx >= n and not available:
            return True

        current_time = heapq.heappop(machines)

        if not available and idx < n and current_time < tasks[idx][0]:
            current_time = tasks[idx][0]

        while idx < n and tasks[idx][0] <= current_time:
            release_time, latest_start = tasks[idx]
            heapq.heappush(available, (latest_start, release_time))
            idx += 1

        if not available:
            heapq.heappush(machines, current_time)
            continue

        latest_start, _release = heapq.heappop(available)
        if current_time > latest_start:
            return False

        heapq.heappush(machines, current_time + task_length)


def prob3(start_times: list[int], task_length: int, deadlines: list[int]) -> int:
    """
    Return the minimum number of CPUs required so that each task finishes
    by its own deadline, or -1 if impossible.
    """
    n = len(start_times)
    if n != len(deadlines):
        raise ValueError("start_times and deadlines must have the same length")
    if n == 0:
        return 0

    if task_length < 0:
        raise ValueError("task_length must be non-negative")

    if task_length == 0:
        # Zero-length tasks only need release <= deadline
        return -1 if any(s > d for s, d in zip(start_times, deadlines)) else 1

    tasks: list[tuple[int, int]] = []
    for start_time, deadline in zip(start_times, deadlines):
        latest_start = deadline - task_length
        if latest_start < start_time:
            return -1
        tasks.append((start_time, latest_start))

    tasks.sort(key=lambda x: x[0])

    left, right = 1, n
    while left < right:
        mid = (left + right) // 2
        if _feasible_with_k(tasks, task_length, mid):
            right = mid
        else:
            left = mid + 1

    return left
