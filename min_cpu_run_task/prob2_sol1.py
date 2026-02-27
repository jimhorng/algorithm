"""
Problem 2: Variable Duration, Minimize End Time
Approach: Binary search on CPU count + greedy simulation with min-heap

Key observations:
1. min_possible_end = max(start_times[i] + task_lengths[i]) over all i
   (the earliest end achievable if every task started at its nominal time)
2. Binary search on k (number of CPUs).
3. Simulate: sort tasks by (start, -length), then greedily assign each
   task to the CPU available earliest via min-heap.
4. A task delayed to time t starts at t and ends at t + task_lengths[i].
   If end > min_possible_end for any task, this k is infeasible.

Sort order: (start_time, -task_length) -- longer tasks first within the
same start time. This ensures longer (harder to delay) tasks are scheduled
first while CPUs are all available, leaving slack for shorter tasks.

Known limitation:
  The (start, -length) sort is a heuristic. It fails when the optimal
  schedule requires a SHORT task to be chained BEFORE a longer one sharing
  the same start time, in order to free a CPU early enough for a later task.

  Counter-example:
    start_times=[2,2,4,5,9], task_lengths=[1,6,8,2,6]  -> expected 2, returns 3
    Optimal:  CPU1: (4,8)[4-12] + (5,2)[12-14]
              CPU2: (2,1)[2-3]  + (2,6)[3-9] + (9,6)[9-15]
    Sol1 forces (2,6) before (2,1) and never finds this schedule.

Time Complexity: O(n log n)
  - Sorting:       O(n log n)  -- once
  - Binary search: O(log n) iterations x O(n log k) simulation = O(n log n)
Space Complexity: O(n) for sorted_tasks + O(k) heap
"""

import heapq


def _simulate(sorted_tasks, num_cpus, min_possible_end):
    """
    Greedily assign tasks to `num_cpus` CPUs.
    Returns True if all tasks finish by min_possible_end.
    """
    cpu_times = [0] * num_cpus   # min-heap: each entry = time CPU becomes free
    heapq.heapify(cpu_times)

    for start, length in sorted_tasks:
        earliest_available = heapq.heappop(cpu_times)
        actual_start = max(start, earliest_available)
        end_time = actual_start + length

        if end_time > min_possible_end:
            return False                     # this k cannot achieve min end time

        heapq.heappush(cpu_times, end_time)

    return True


def _binary_search_min_cpus(sorted_tasks, min_possible_end):
    n = len(sorted_tasks)
    left, right = 1, n
    result = n

    while left <= right:
        mid = (left + right) // 2
        if _simulate(sorted_tasks, mid, min_possible_end):
            result = mid
            right = mid - 1
        else:
            left = mid + 1

    return result


def prob2(start_times, task_lengths):
    if not start_times:
        return 0

    # Sort by (start_time, -task_length): schedule longer tasks first
    # within the same start time so shorter tasks absorb any delays
    sorted_tasks = sorted(
        zip(start_times, task_lengths),
        key=lambda x: (x[0], -x[1])
    )

    # Lower bound: every task runs unobstructed from its earliest start
    min_possible_end = max(s + l for s, l in sorted_tasks)

    return _binary_search_min_cpus(sorted_tasks, min_possible_end)
