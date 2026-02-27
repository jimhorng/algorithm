"""
Problem 2: Variable Duration, Minimize End Time
Approach: Backward exhaustive DFS -- try all prepend options

Core idea
---------
Sort tasks by start_time DESC (process latest-starting tasks first).
Each CPU is represented by its current "front time" -- the start of the
earliest task placed on it so far.

For each task (s, l) we consider EVERY possible placement:
  Option A -- prepend to an existing CPU i:
    condition : cpu_fronts[i] >= s + l
    result    : cpu_fronts[i] becomes cpu_fronts[i] - l   (right-justified)
    Right-justifying the prepend pushes the task as far right as possible,
    maximising the remaining left window for even-earlier future tasks.
    (cpu_fronts[i] - l >= s is guaranteed by the condition.)
  Option B -- open a new CPU right-justified to the deadline:
    result    : add a CPU with front = mpe - l
    ("append up to total deadline" -- fills right up to the common deadline)

We branch on all valid options and recurse, returning the minimum total CPUs.

Symmetry breaking: if two placement choices lead to the same sorted tuple
of CPU fronts, we only explore one of them. Deduplication is done via the
resulting state (sorted fronts tuple), not the front values tried.

Memoisation: the state is (task_index, sorted tuple of cpu_fronts).
This is the same proof-of-correctness structure as sol3, but using the
backward ordering + right-justify framing instead of forward ERF pruning.

Time Complexity
---------------
Let  n     = number of tasks
     L_max = max task length
     V     = number of distinct front values that can appear
           = number of distinct subset sums of task lengths that fit in [0, mpe]
           ≤ min(2^n,  n · L_max + 1)

State space:
  A state is (i, fronts) where fronts is a sorted tuple of ≤ i CPU front
  times.  Each front is mpe minus the sum of lengths of tasks on that CPU,
  so every front value comes from a subset sum of the task lengths → at most
  V distinct values per slot.

  The number of distinct sorted k-tuples from V values (multisets of size k)
  is C(V+k-1, k).  Summing over k = 0..n:
    Σ_{k=0}^{n} C(V+k-1, k) = C(V+n, n)
  Multiplied by n task-index positions:
    Total states ≤ n · C(V+n, n)

Per-state work:
  At each state there are at most n branches (one per existing CPU plus the
  new-CPU option).  Building the new sorted fronts tuple costs O(n log n).
  → O(n log n) per state.

Overall:  O(n² log n · C(V+n, n))

Practical notes:
  • Without memoisation the recursion tree has up to O((n+1)!) leaves;
    memoisation collapses it to the polynomial-in-V state count above.
  • When all task lengths are equal (V = 1), C(1+n, n) = n+1 and the
    algorithm runs in O(n³ log n) -- nearly linear in practice.
  • When task lengths are small integers (L_max ≤ ~20, n ≤ ~15) the
    algorithm is fast; for large/varied lengths it can approach exponential.

Space Complexity: O(n · C(V+n, n)) -- one cache entry per state
"""

from functools import lru_cache


def prob2(start_times, task_lengths):
    if not start_times:
        return 0

    # Sort tasks latest-starting first; among ties, longer tasks first
    sorted_tasks = tuple(sorted(
        zip(start_times, task_lengths),
        key=lambda x: (-x[0], -x[1])
    ))

    mpe = max(s + l for s, l in sorted_tasks)  # min possible end time

    @lru_cache(maxsize=None)
    def dfs(i, fronts):
        """
        i      : index into sorted_tasks (0 = latest task)
        fronts : sorted tuple of CPU front times assigned so far
        Returns: minimum number of CPUs needed for tasks[i:]
        """
        if i == len(sorted_tasks):
            return len(fronts)

        s, l = sorted_tasks[i]
        best = len(sorted_tasks)           # upper bound: one CPU per task
        seen_states = set()                # avoid identical resulting states

        # Option A: prepend to each existing CPU whose front >= s + l
        for j, front in enumerate(fronts):
            if front >= s + l:
                # Right-justify: start as late as possible → front - l
                # (front - l >= s is guaranteed by the condition above)
                new_fronts = tuple(sorted(fronts[:j] + (front - l,) + fronts[j+1:]))
                if new_fronts not in seen_states:
                    seen_states.add(new_fronts)
                    best = min(best, dfs(i + 1, new_fronts))

        # Option B: open a new CPU, right-justified at mpe - l
        new_fronts = tuple(sorted(fronts + (mpe - l,)))
        if new_fronts not in seen_states:
            seen_states.add(new_fronts)
            best = min(best, dfs(i + 1, new_fronts))

        return best

    return dfs(0, ())

