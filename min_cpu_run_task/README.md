## Problem 1 — Fixed Duration, Minimize End Time

Given a list of start times for tasks. **Each task has the same length**, find the min number of CPUs needed to **minimize the end time of the final task**.

Each task can start on or after its start time.

```
Example 1:
  start_times = [0, 0, 0, 10000],  task_length = 5
  output: 1   (large gap lets tasks run sequentially)

Example 2:
  start_times = [0, 0, 0],  task_length = 5
  output: 3   (all must start at 0, need 3 CPUs)
```

### Solutions

#### prob1_sol1 — Forward with Binary Search · [prob1_sol1.py](prob1_sol1.py)

1. Sort start times in increasing order.
2. `min_possible_end = last_start_time + task_length`
3. Binary search on k (1..n); simulate greedy assignment to earliest-available CPU via deque.
4. Early stop: if the last task is delayed past its start time, k fails.

- Time: O(n log n) — sorting once + O(log n) × O(n) simulation
- Space: O(n)
- Key insight: deque stays naturally sorted, giving O(1) operations.

#### prob1_sol2 — Backward with Max Heap · [prob1_sol2.py](prob1_sol2.py)

1. Sort start times; process tasks last → first.
2. Max heap tracks the latest "free time boundary" per CPU.
3. Greedily reuse CPU with largest free time; move boundary back by `task_length`.

- Time: O(n log n)
- Space: O(k)
- Key insight: backward processing eliminates binary search — working from the fixed endpoint allows direct minimization.

#### prob1_sol3 — Forward min-heap, no binary search · [prob1_sol3.py](prob1_sol3.py)

1. Sort tasks by start_time.
2. Min-heap of CPU free times; for each task `s`: compute `actual_start = max(cpu_free, s)`, `end = actual_start + L`.
3. If `end <= final_deadline` → reuse (pop and push `end`), else open new CPU (push `s + L`).

Identical to the inner `_simulate()` of sol1, but run once without a binary-search cap on the number of CPUs.

- Time: O(n log n) · Space: O(n)
- ⚠ Incorrect on some inputs — see Known Failure

### ⚠ Known Failure (sol3 only)

When a task fits on the earliest-free CPU `(actual_start + L ≤ final_deadline)`, sol3 always reuses it. This can advance that CPU's free time past the start of later tight-deadline tasks that needed an early slot.

  Counter-example: `start_times=[0,0,0,...,20]*10`, `task_length=6` → expected **20**, sol3 returns **30**. Also: `start_times=[0,4,9,9]`, `task_length=5` → expected **2**, sol3 returns **3** (reuses CPU for `s=4` task advancing free to 10; both `s=9` tasks then can't chain on it).

  Root cause: same class of flaw as prob2_sol1/sol2 and prob3_sol1 — greedy reuse sacrifices future flexibility for tight-deadline tasks.

### Test Cases · [prob1_test_cases.py](prob1_test_cases.py)
8 cases: single task, no-overlap, full-overlap, partial-overlap, 50-task scale test.

---

## Problem 2 — Variable Duration, Minimize End Time

Given a list of start times and **corresponding task durations**, find the min number of CPUs needed to **minimize the end time of the final task**.

```
Example:
  start_times  = [0, 0, 5]
  task_lengths = [10, 5, 3]
  output: 2
    CPU1: task0[0-10]
    CPU2: task1[0-5], task2[5-8]   final end = 10
```

**Key difference from P1**: each task has its own duration; greedy ordering choices are no longer straightforward.

`min_possible_end = max(start_times[i] + task_lengths[i])` — the lower bound if every task starts at its earliest.

#### prob2_sol1 — Binary Search + Min-Heap · [prob2_sol1.py](prob2_sol1.py)

Sort by `(start_time, -task_length)`. Binary search on k; simulate by assigning each task to the earliest-available CPU via min-heap. If any `actual_start + length > min_possible_end`, k fails.

- Time: O(n log n) · Space: O(n)
- ⚠ Incorrect on some inputs — see [Failure 2: sort order heuristic](#failure-2--sort-order-heuristic-is-not-globally-optimal)

#### prob2_sol2 — Direct Greedy, No Binary Search · [prob2_sol2.py](prob2_sol2.py)

Same sort. Single pass: peek at the earliest-available CPU — reuse if it fits, otherwise allocate a new CPU (task runs from its nominal start).

- Time: O(n log n) · Space: O(k)
- ⚠ Incorrect on some inputs — see [Failure 1: greedy reuse](#failure-1--greedy-reuse-is-not-globally-optimal) and [Failure 2: sort order heuristic](#failure-2--sort-order-heuristic-is-not-globally-optimal)

#### prob2_sol3 — Backtracking + Binary Search (Correct) · [prob2_sol3.py](prob2_sol3.py)

Binary search on k. For each candidate k, backtracking tries all ways to partition tasks into k groups. Each group is validated by Earliest-Release-First (ERF) simulation. ERF is provably optimal for single-machine scheduling with a common deadline (exchange-argument proof), so rejecting an ERF-infeasible group is sound. Symmetry breaking skips duplicate CPU states to prune the search tree.

- Time: O(log n · k^n · n log n) worst case — exponential, but aggressively pruned in practice
- Correct: passes all 9 test cases including the two known failure cases for sol1/sol2
- Trade-off: correct for arbitrary inputs at the cost of potentially exponential time; use sol1 for large inputs where approximate answers are acceptable

#### prob2_sol4 — Backward Exhaustive DFS + Right-Justify · [prob2_sol4.py](prob2_sol4.py)

Sort tasks by start_time DESC. Each CPU tracks its current "front time" — the start of its leftmost placed task. For each task `(s, l)` exhaust all placements:
- **Option A** – prepend to any CPU with `front ≥ s + l`: set `new_front = front - l` (right-justified, pushes task as late as possible to maximise the gap for earlier tasks)
- **Option B** – open a new CPU right-justified at `mpe - l`

Takes the minimum across all branches with memoisation on `(task_idx, sorted cpu_fronts tuple)`.

- Correct: passes all 9/9 tests and 5000-trial stress test vs brute force
- Time: O(n² log n · C(V+n, n)) where V = min(2^n, n·L_max+1) is the number of distinct CPU front values (subset sums of task lengths); memoisation collapses the O((n+1)!) recursion tree to this state count
- Space: O(n · C(V+n, n))

### ⚠ Known Failures (sol1 / sol2 only — sol3 is correct)

#### Failure 1 — Greedy reuse is not globally optimal

> Affects: **prob2_sol2** only · prob2_sol1 handles this correctly

Counter-example: `start_times=[0,4,6,7,8]`, `task_lengths=[7,5,8,6,4]` → expected **3**, prob2_sol2 returns **4**

`min_possible_end = 14`. Sol2 reuses the only CPU for `(4,5)` after `(0,7)` (end=12 ≤ 14). That CPU is now free at 12, and every remaining task exceeds 14 on it — each forces a new CPU.

Optimal: put `(4,5)` on a **new** CPU so the original CPU stays free at 7 for `(7,6)`:
```
CPU1: (0,7)[0-7]  + (7,6)[7-13]
CPU2: (4,5)[4-9]  + (8,4)[9-13]
CPU3: (6,8)[6-14]
```
Sol2 has no look-ahead — "earliest CPU fits" ≠ "best CPU to reuse". prob2_sol1 handles this by validating the full schedule at a fixed k=3.

#### Failure 2 — Sort order heuristic is not globally optimal

> Affects: **both sols** · no known O(n log n) greedy fix exists

Counter-example: `start_times=[2,2,4,5,9]`, `task_lengths=[1,6,8,2,6]` → expected **2**, both return **3**

`min_possible_end = 15`. Optimal schedule:
```
CPU1: (4,8)[4-12] + (5,2)[12-14]
CPU2: (2,1)[2-3]  + (2,6)[3-9]  + (9,6)[9-15]
```
This requires the **short** task `(2,1)` chained **before** the long `(2,6)` on the same CPU. But `(start, -length)` always processes `(2,6)` first, locking that CPU until ~8 and preventing `(9,6)` from fitting in the chain.

Root cause: the sort heuristic "harder tasks first" can miss schedules where a short task acts as a bridging step that frees a CPU for a much-later task. No fixed sort order guarantees optimality for the general variable-duration case.

> **Why is this hard?** Parallel machine scheduling with release times and a common deadline (Pm|r_j|C_max) is NP-hard in general, so no known polynomial-time algorithm is always correct. prob2_sol3 is the provably correct solution using backtracking.

### Test Cases · [prob2_test_cases.py](prob2_test_cases.py)
9 cases including `sol2_greedy_reuse_fails` and `sort_order_fails_both_sols`.

---

## Problem 3 — Fixed Duration, Per-Task Deadline

Given start times and a **per-task deadline array**, each task has the same length. Find the min CPUs such that **every task finishes at or before its own deadline**. Return -1 if impossible.

Valid start window for task i: `[start_times[i], deadlines[i] - task_length]`

```
Example 1:
  start_times = [0, 0, 0, 10000],  task_length = 5
  deadlines   = [5, 5, 5, 10005]
  output: 3   (tasks 0-2 all pinned to [0-5])

Example 2:
  deadlines = [15, 15, 15, 10005]
  output: 1   (tasks 0-2 can run sequentially at [0,5,10])

Impossible:
  start_times=[10], deadlines=[14], task_length=5
  output: -1   (10+5=15 > 14)
```

**Key difference from P1**: deadline is per-task, not implicit. Some inputs have no solution.

### Solutions

#### prob3_sol1 — Forward start_time + Min-Heap · [prob3_sol1.py](prob3_sol1.py)

Adaptation of prob1_sol1. Sort by `(start_time, deadline)` — same chronological order as prob1. The one meaningful change from prob1: replace the shared global deadline check with a per-task `actual_start + L <= deadline[i]` check. No binary search needed — if the earliest-free CPU fails the deadline, all others (freed later) are worse, so opening a new CPU is the only option.

Sorting by start_time (not deadline/EDF) is essential: a looser-deadline task may need an earlier clock slot so a tighter-deadline task can be pinned later. EDF breaks this by scheduling tight-deadline tasks first.

- Time: O(n log n) · Space: O(n)
- ⚠ Incorrect on some inputs — see [Failure: greedy reuse blocks tight-deadline tasks](#failure--greedy-reuse-blocks-tight-deadline-tasks)

#### prob3_sol2 — Backward, start_time DESC + Max-Heap · [prob3_sol2.py](prob3_sol2.py)

Adaptation of prob1_sol2. Sort by `(-start_time, -deadline)` — reverse chronological order, same as prob1. The key change: effective right boundary = `min(deadline, cpu_front)` — a task cannot exceed its own deadline even if the CPU chain starts later. Condition: `effective >= start + L`, new front = `effective - L`.

Sorting by start_time DESC (not deadline DESC) is essential for the same reason as sol1: deadline-first ordering fails when a looser-deadline task must occupy an earlier slot.

- Time: O(n log n) · Space: O(n)
- ⚠ Incorrect on some inputs — see [Failure: max-front wastes high-front chains](#failure--max-front-greedy-wastes-high-front-chains)

#### prob3_sol3 — Forward + Binary Search · [prob3_sol3.py](prob3_sol3.py)

prob1-style formulation for per-task deadlines.

1. Pre-check impossible tasks: if `start_times[i] + task_length > deadlines[i]` for any i, return `-1`.
2. Transform each task to `(release, latest_start)` where `latest_start = deadline - task_length`.
3. Binary search on `k` (1..n CPUs).
4. Feasibility simulation for fixed `k`:
   - Min-heap `machines`: next-free time per CPU.
   - Min-heap `available`: released tasks ordered by `latest_start`.
   - Repeatedly take earliest-free CPU time `t`, fast-forward if no task is released,
     then run the available task with smallest `latest_start`.
   - If `t > latest_start` for the chosen task, `k` is infeasible.

- Time: O(n log n log n) · Space: O(n)
- Notes: this variant matches prob1's "binary search + forward simulate" pattern
  and passes current 12/12 `prob3_test_cases.py`.

### ⚠ Known Failures

#### Failure — Forward sol1: greedy reuse blocks tight-deadline tasks

> Affects: **prob3_sol1** only

Minimal counter-example: `start_times=[0,0,6,6]`, `task_length=5`, `deadlines=[20,20,11,11]` → expected **2**, sol1 returns **3**

Sol1 reuses the same CPU for the second flexible task (d=20), advancing its free time to 10. The tight-deadline tasks (d=11) then find no CPU free at ≤6 → open 2 new CPUs.

#### Failure — max-front greedy wastes high-front chains

> Affects: **prob3_sol2** only

Minimal counter-example: `start_times=[3,3,3,10]`, `task_length=5`, `deadlines=[12,13,10,17]` → expected **2**, sol2 returns **3**

Sol2 processes tasks backward: T3(10,17) → T1(3,13) → T0(3,12) → T2(3,10). T1 is attached to the T3 chain (max_front=12, effective=12≥8✓), dropping front to 7. T0 and T2 then need effective≧8 but see only front=7 → two new CPUs opened.

**Optimal (2 CPUs):** `CPU1: T2[3,8]→T3[10,15]`, `CPU2: T0[3,8]→T1[8,13]`. T0 and T1 share the same start time and can chain sequentially (T1 starts at max(8,3)=8, ends 13≤13✓). Sol2 missed this by greedily consuming the high-front slot for T1 instead.

**Root cause:** always reusing the most-attractive slot (highest front) destroys its utility for tasks that needed it, identical in structure to sol1’s and prob2’s greedy reuse flaw.

### Test Cases · [prob3_test_cases.py](prob3_test_cases.py)
12 cases: 8 core cases, 2 EDF-failure cases (`edf_fails_*`), 1 sol1 failure (`sol1_greedy_reuse_*`), 1 sol2 failure (`sol2_max_front_*`).

---

## Problem 4 — Variable Duration, Per-Task Deadline

Given start times, **per-task durations**, and a **per-task deadline array**. Find the min CPUs such that **every task finishes at or before its own deadline**. Return -1 if impossible.

Valid start window for task i: `[start_times[i], deadlines[i] - task_lengths[i]]`

```
Example 1:
  start_times  = [0, 0, 5],  task_lengths = [10, 5, 3]
  deadlines    = [10, 10, 10]
  output: 2   (CPU1: task0[0-10]; CPU2: task1[0-5], task2[5-8])

Impossible:
  start_times=[5], task_lengths=[3], deadlines=[7]
  output: -1   (5+3=8 > 7)
```

**Key difference**: most general form — combines variable durations with per-task deadlines. Interval graph coloring with variable-length jobs.

### Solution Approach (TODO)
- Feasibility check: if `start_times[i] + task_lengths[i] > deadlines[i]` for any i → return -1
- Each task has window `[start_times[i], deadlines[i] - task_lengths[i]]` with length `task_lengths[i]`
- Sweep line or interval DP; more complex than P3 due to variable lengths

### Test Cases · [prob4_test_cases.py](prob4_test_cases.py)
9 cases: exact-fit windows, impossible windows, overlap forcing parallel, optimal interleaving.

---

## How to Run

```bash
# Canonical Python entrypoint in every solution module:
# prob1(...), prob2(...), prob3(...)

# One problem, all its default solutions
python3 main.py prob=1
python3 main.py prob=2

# One problem, specific solution
python3 main.py prob=1 sol=prob1_sol1
python3 main.py prob=1 sol=prob1_sol2
python3 main.py prob=2 sol=prob2_sol1
python3 main.py prob=2 sol=prob2_sol2
python3 main.py prob=2 sol=prob2_sol3
python3 main.py prob=2 sol=prob2_sol4
python3 main.py prob=3 sol=prob3_sol1
python3 main.py prob=3 sol=prob3_sol2
python3 main.py prob=3 sol=prob3_sol3
```

### Project Structure
```
min_cpu_run_task/
├── README.md              # This file
├── main.py                # Unified test runner (all problems)
├── prob1_sol1.py          # P1: Forward with binary search + deque
├── prob1_sol2.py          # P1: Backward with max heap
├── prob1_sol3.py          # P1: Forward greedy min-heap, no binary search (7/8, reuse over-chains)
├── prob1_test_cases.py    # P1: Test cases
├── Main.java              # P1: Java (TreeMap approach)
├── MainMaxHeap.java       # P1: Java (Max heap approach)
├── prob2_sol1.py          # P2: Binary search + min-heap (fast, mostly correct)
├── prob2_sol2.py          # P2: Direct greedy, no binary search (fast, partially correct)
├── prob2_sol3.py          # P2: Backtracking + binary search (correct)
├── prob2_sol4.py          # P2: Backward exhaustive DFS + right-justify (correct)
├── prob2_test_cases.py    # P2: Test cases
├── prob3_sol1.py          # P3: Forward start_time + min-heap
├── prob3_sol2.py          # P3: Backward start_time DESC + max-heap
├── prob3_sol3.py          # P3: Forward + binary search (release/latest-start heaps)
├── prob3_test_cases.py    # P3: Test cases
└── prob4_test_cases.py    # P4: Test cases (impl TODO)
```

---

## Implementation Status

- ✅ **Problem 1**: sol1 and sol2 correct (12/12); sol3 fails 2 cases — greedy reuse over-chains early tasks, blocking CPUs from tight-deadline tasks (see Known Failure)
- ✅ **Problem 2**: sol3_problem2.py is correct (9/9); sol1 fails 1 case, sol2 fails 2 cases (see Known Failures)
- ⏳ **Problem 3**: sol1 and sol2 each fail 1 case (different modes); sol3 implements forward+binary-search and passes current 12/12 tests
- ⏳ **Problem 4**: Test cases ready, implementation TODO
