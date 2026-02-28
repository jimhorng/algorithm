"""
Problem 3: Fixed Duration, Per-Task Deadline
Approach: Backward greedy -- sort by start_time DESC + max-heap of front times

Algorithm
---------
1. Pre-check: any s + L > d -> return -1.
2. Sort tasks by start_time DESC; ties broken by deadline DESC.
3. Max-heap of CPU front times (negated for Python's min-heap).
4. For each task (start, deadline):
     F         = max front (-heap[0])
     effective = min(deadline, F)
     if effective >= start + L:
         pop F; push -(effective - L)    # prepend to this CPU
     else:
         push -(deadline - L)            # new CPU, right-justified
5. Return len(heap).

Time Complexity : O(n log n)  -- sort + n heap operations
Space Complexity: O(n)
"""

import heapq


def prob3(start_times, task_length, deadlines):
    if not start_times:
        return 0

    # Pre-check
    if any(s + task_length > d for s, d in zip(start_times, deadlines)):
        return -1

    # Sort by start_time DESC, ties by deadline DESC -- same direction as prob1
    tasks = sorted(
        zip(start_times, deadlines),
        key=lambda x: (-x[0], -x[1])
    )

    cpu_heap = []  # max-heap (negate values) of CPU front times

    for start, deadline in tasks:
        if cpu_heap:
            max_front = -cpu_heap[0]
            effective = min(deadline, max_front)
            if effective >= start + task_length:
                heapq.heappop(cpu_heap)
                heapq.heappush(cpu_heap, -(effective - task_length))
                continue
        # No existing CPU qualifies -- open a new one, right-justified to deadline
        heapq.heappush(cpu_heap, -(deadline - task_length))

    return len(cpu_heap)
