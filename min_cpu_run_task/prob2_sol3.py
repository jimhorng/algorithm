"""
Problem 2 — Solution 3: Backtracking + Binary Search (Correct)
================================================================
Approach
--------
Binary search on k (minimum CPUs), and for each k verify feasibility via
backtracking over all possible task-to-CPU assignments.

Key theorem (used to prune the backtracking):
    For a single machine with release times and a COMMON deadline T,
    Earliest-Release-First (ERF) is optimal * — i.e., if ERF fails for
    a given set of tasks on one CPU, no other ordering can succeed.

    * Proof (exchange argument): consider two tasks i, j with r_i <= r_j
      scheduled consecutively starting at time t.
        ERF  end (i first): max(r_j, r_i+p_i) + p_j
        non-ERF end (j first): r_j + p_j + p_i
      max(r_j, r_i+p_i) <= r_j + p_i always holds (both cases: r_j >= r_i+p_i
      or r_j < r_i+p_i). So ERF never increases the last completion time.
      By transitivity over all pairs, ERF minimises the last completion time
      for any number of tasks on a single machine.

Backtracking strategy
---------------------
1. Sort tasks by *tightest window first* (latest_start asc) so highly
   constrained tasks are placed early, enabling fast pruning.
2. For each task (in that order) try each CPU group:
   - Append the task to the group.
   - Run ERF simulation; if it violates the deadline, prune and try next CPU.
   - Symmetry breaking: identical CPU states are skipped (avoids redundant work).
3. If all tasks are placed successfully, feasibility is confirmed.

Binary search over k gives the minimum number of CPUs.

Complexity
----------
Worst case: O(log n · k^n · n log n)   — exponential in n for fixed k.
In practice, aggressive pruning keeps this fast for n ≤ ~15.

Why is this hard? (Optional context)
--------------------------------------
The general Pm|r_j|C_max problem (parallel machines, release times, minimise
makespan) is NP-hard; our feasibility formulation is equivalent, so no known
polynomial algorithm exists for arbitrary inputs. sol1 and sol2 are fast
heuristics that fail on specific edge cases. sol3 is correct at the cost of
potentially exponential time.
"""

import heapq


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _erf_feasible(cpu_tasks: list, mpe: int) -> bool:
    """
    Check if tasks assigned to one CPU can all finish by `mpe`.
    Schedules them in Earliest-Release-First order (proved optimal for
    single-machine, common-deadline feasibility).
    """
    t = 0
    for start, length in sorted(cpu_tasks, key=lambda x: x[0]):
        t = max(t, start) + length
        if t > mpe:
            return False
    return True


def _can_schedule_k(ordered_tasks: list, k: int, mpe: int) -> bool:
    """
    Backtracking feasibility check: can `k` CPUs handle all tasks by `mpe`?

    `ordered_tasks` are sorted by (latest_start asc, start asc) so the most
    constrained tasks are tried first for fast pruning.
    """
    groups: list[list] = [[] for _ in range(k)]

    def backtrack(i: int) -> bool:
        if i == len(ordered_tasks):
            return True
        task = ordered_tasks[i]
        seen_states: set = set()
        for g in range(k):
            # Symmetry breaking: skip CPUs that are in an identical state
            state = tuple(sorted(groups[g]))
            if state in seen_states:
                continue
            seen_states.add(state)

            groups[g].append(task)
            if _erf_feasible(groups[g], mpe):
                if backtrack(i + 1):
                    return True
            groups[g].pop()
        return False

    return backtrack(0)


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

def prob2(start_times: list[int], task_lengths: list[int]) -> int:
    """
    Return the minimum number of CPUs so that every task can be scheduled
    within the optimal makespan window.

    Parameters
    ----------
    start_times  : earliest start time for task i
    task_lengths : processing time for task i

    Returns
    -------
    Minimum number of CPUs required.
    """
    if not start_times:
        return 0

    tasks = list(zip(start_times, task_lengths))
    mpe = max(s + l for s, l in tasks)          # minimum possible end time
    n = len(tasks)

    # Sort once: tightest deadline (smallest latest_start) first
    ordered = sorted(tasks, key=lambda x: (mpe - x[1], x[0]))

    # Binary search on k
    lo, hi, result = 1, n, n
    while lo <= hi:
        mid = (lo + hi) // 2
        if _can_schedule_k(ordered, mid, mpe):
            result = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return result
