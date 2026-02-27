"""
Problem 3: Fixed Duration, Per-Task Deadline
Approach: Backward greedy -- sort by start_time DESC + max-heap of front times

Key differences from prob1_sol2
---------------------------------
prob1_sol2 processes tasks by start_time DESC and right-justifies every task
to a single shared boundary (max_start_time).  In prob3 each task has its own
deadline, so the right boundary differs per task.

Sort order: SAME as prob1 -- start_time DESC (not deadline DESC).
  Sorting by deadline DESC fails when a looser-deadline task must occupy an
  earlier clock slot to make room for a pinned tight-deadline task.

  Counter-example for deadline DESC:
    starts=[0, 5], L=3, deadlines=[9, 8]
    T1(s=5,d=8) pinned at [5,8]. T0(s=0,d=9) must run at [0,3].
    Deadline DESC processes T0 first -> placed at [6,9] (right-justified).
    CPU front=6. T1: min(8,6)=6, 6 >= 5+3=8? No -> 2nd CPU. WRONG.
    start_time DESC: T1 processed first -> right-justified at [5,8], front=5.
    T0: min(9,5)=5 >= 0+3 -> prepend, front=2. 1 CPU. CORRECT.

The only actual change vs prob1_sol2:
  effective right boundary = min(deadline, cpu_front) instead of a fixed
  shared max_start_time.  This caps each placement at the task's own deadline.

  effective  = min(deadline, cpu_front)
  condition  : effective >= start + L
  new_front  : effective - L

For a new CPU (no existing CPU qualifies), right-justify to the task's own
deadline: front = deadline - L.

Known Failure — max-front greedy wastes high-front chains
---------------------------------------------------------
Always picking the CPU with the HIGHEST front is not globally optimal.
Attaching a loose-deadline task to the max-front chain lowers that chain's
front, which can block earlier-starting tasks that needed a high front to fit.

  Counter-example: starts=[3,3,3,10], L=5, deadlines=[12,13,10,17]
    Processing order (start DESC, deadline DESC): T3(10,17), T1(3,13), T0(3,12), T2(3,10)
    T3(10,17): new CPU A, front=12.
    T1(3,13): reuse A (max_front=12, effective=12>=8 ✓), front=7.
    T0(3,12): effective=min(12,7)=7 < 8 → new CPU B, front=7.
    T2(3,10): effective=min(10,7)=7 < 8 → new CPU C, front=5.  Returns 3.

    Optimal (2 CPUs): CPU1: T2[3,8]→T3[10,15]; CPU2: T0[3,8]→T1[8,13].
    T0 and T1 share start=3 but can be chained sequentially (T0 ends at 8,
    T1 starts at max(8,3)=8, ends 13≤13 ✓).  Sol2 missed this because it
    greedily attached T1 to the high-front T3 chain, exhausting that slot.

  Root cause: same structural flaw as sol1/prob2 — always reusing the
  most-attractive slot (here: max front) blocks future tasks that needed it.

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
