"""
Problem 2: Variable Duration, Minimize End Time
Approach: Direct greedy with min-heap -- no binary search needed

Key idea:
  Process tasks sorted by (start_time, -task_length).
  Maintain a min-heap of CPU "available at" times.

  For each task (start, length):
    1. Peek at the earliest-available CPU (heap min).
    2. actual_start = max(start, cpu_available)
       end_time    = actual_start + length
    3. If end_time <= min_possible_end:
         Reuse this CPU -- pop it and push end_time.
    4. Else:
         No existing CPU can accommodate this task without exceeding the
         deadline. Add a new CPU: push start + length (task starts at its
         earliest nominal time on a fresh CPU).

Correctness of "new CPU" branch: The earliest-available CPU gives the
smallest possible actual_start. If even that CPU causes end > min_possible_end,
no existing CPU can do better -- a new CPU is necessary.  ✓

Sort order: (start_time, -task_length) -- longer tasks first within the same
start time; longer tasks are harder to delay, so assign them while CPUs are free.

Time Complexity: O(n log n)  -- one pass, each step is O(log k) heap op
Space Complexity: O(k)        -- heap holds one entry per CPU
"""

import heapq


def prob2(start_times, task_lengths):
    if not start_times:
        return 0

    sorted_tasks = sorted(
        zip(start_times, task_lengths),
        key=lambda x: (x[0], -x[1])
    )

    min_possible_end = max(s + l for s, l in sorted_tasks)

    cpu_times = []  # min-heap of CPU available times

    for start, length in sorted_tasks:
        if cpu_times:
            earliest_available = cpu_times[0]       # peek min (no pop yet)
            actual_start = max(start, earliest_available)
            end_time = actual_start + length

            if end_time <= min_possible_end:
                heapq.heappop(cpu_times)             # consume this CPU slot
                heapq.heappush(cpu_times, end_time)
                continue

        # No existing CPU works (or heap is empty): allocate a new CPU.
        # Task runs from its earliest nominal start on a fresh CPU.
        heapq.heappush(cpu_times, start + length)

    return len(cpu_times)
