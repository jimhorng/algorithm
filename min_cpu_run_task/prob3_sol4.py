"""
Problem 3 — Solution 4: Hall's Condition + Binary Search
==========================================================

Algorithm
---------
For k identical machines and n jobs of equal length L with release times r_i
and deadlines d_i, a feasible non-preemptive schedule exists if and only if
**Hall's condition** holds for every time interval [a, b):

    |{ i : r_i >= a  AND  d_i <= b }|  <=  k * floor((b - a) / L)

In plain terms: the number of tasks that must execute entirely within [a, b)
cannot exceed the total slot capacity of k machines in that window.

This is both *necessary* (obvious capacity argument) and *sufficient* (follows
from the bipartite-matching / LP-integrality theorem for uniform-length jobs on
identical parallel machines).  Unlike EDF or EDD greedy algorithms, it correctly
handles cases that require "strategic idling" — an idle gap before a
tight-deadline task to avoid blocking it with a looser-deadline task.

Steps:
1) Pre-check impossibility: if start_i + L > deadline_i for any task -> -1.
2) Binary-search on k in [1, n].
3) For fixed k, check Hall's condition over all O(n^2) critical-point pairs.
   Critical points: { r_i } ∪ { d_i } (at most 2n distinct values).

Time Complexity : O(n^3 log n) — O(n^2) pairs × O(n) count × O(log n) binary search
Space Complexity: O(n)
"""

from __future__ import annotations


def _feasible_with_k(tasks: list[tuple[int, int]], task_length: int, num_cpus: int) -> bool:
    """
    Hall's condition for identical-job parallel machine scheduling.

    tasks : list of (release_time, latest_start).
    Returns True iff, for every interval [a, b) formed by critical points,
    the number of tasks contained within it does not exceed
    num_cpus * floor((b - a) / task_length).
    """
    releases = [r for r, _ in tasks]
    deadlines = [ls + task_length for _, ls in tasks]
    critical = sorted(set(releases + deadlines))

    for ai, a in enumerate(critical):
        for b in critical[ai + 1:]:
            capacity = num_cpus * ((b - a) // task_length)
            demand = sum(1 for r, d in zip(releases, deadlines) if r >= a and d <= b)
            if demand > capacity:
                return False
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

    left, right = 1, n
    while left < right:
        mid = (left + right) // 2
        if _feasible_with_k(tasks, task_length, mid):
            right = mid
        else:
            left = mid + 1

    return left