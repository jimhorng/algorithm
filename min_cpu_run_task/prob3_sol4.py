from __future__ import annotations

import heapq
from typing import List


def prob3(start_times: list[int], task_length: int, deadlines: list[int]) -> int:
    """
    Solution A:
      - Precheck impossibility (latest_start < release)
      - Binary search min CPUs m
      - Feasibility check for fixed m using:
          * machines: min-heap of next-free times
          * available jobs: min-heap keyed by latest_start (deadline - p)
        Always schedule on the earliest-free machine at time t the available job
        with the smallest latest_start.

    Returns:
      - min CPUs if feasible
      - -1 if impossible
    """
    n = len(start_times)
    if n != len(deadlines):
        raise ValueError("start_times and deadlines must have the same length")
    if n == 0:
        return 0
    p = task_length
    if p < 0:
        raise ValueError("task_length must be non-negative")
    if p == 0:
        # zero-length tasks: only need to start within [r, d], always schedulable on 1 CPU if r<=d
        for r, d in zip(start_times, deadlines):
            if r > d:
                return -1
        return 1

    # Build jobs: (release, latest_start)
    jobs = []
    for r, d in zip(start_times, deadlines):
        ls = d - p
        if ls < r:
            return -1
        jobs.append((r, ls))

    jobs.sort(key=lambda x: x[0])  # sort by release time

    def feasible(m: int) -> bool:
        # Min-heap of machine next-free times
        machines = [0] * m
        heapq.heapify(machines)

        # Min-heap of available jobs by latest_start: (latest_start, release)
        available: list[tuple[int, int]] = []

        i = 0  # pointer into jobs

        while True:
            if i >= n and not available:
                return True  # all scheduled

            t = heapq.heappop(machines)

            # If nothing is available yet, fast-forward to next release (keeping CPU idle)
            if not available and i < n and t < jobs[i][0]:
                t = jobs[i][0]

            # Add all jobs released by time t
            while i < n and jobs[i][0] <= t:
                r, ls = jobs[i]
                heapq.heappush(available, (ls, r))
                i += 1

            if not available:
                # No jobs exist at this time and no future jobs (since i>=n handled above)
                heapq.heappush(machines, t)
                continue

            ls, r = heapq.heappop(available)

            # Must be able to start by ls
            if t > ls:
                return False

            # Schedule this job on this machine at time t (non-preemptive)
            heapq.heappush(machines, t + p)

    # Binary search min m in [1, n]
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo