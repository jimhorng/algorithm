## < Problem >
Given a list of start times for a task. Each task has the same length, find the min number of cpus needed to minimize the end time of the final task. 

Each task can start on or after the start time. 

Example 1: 
```
start times = [0,0,0,10000] with
task length t = 5. 
The answer would just be 1
```

Example 2:
```
start times = [0,0,0]
t = 5. 
out: 3
```

## Solution

### Algorithm (sol1) - Forward with Binary Search
Uses binary search with greedy scheduling simulation:
- code: [sol1.py](sol1.py)

1. **Sort start times** in increasing order
2. **Calculate minimum possible end time**: `last_start_time + task_length`
3. **Binary search** for minimum CPUs needed (1 to n)
4. **Simulation**: For each CPU count, greedily assign tasks to earliest available CPU using deque
5. **Early stopping**: If the last task can't start on time, return False

**Time Complexity**: O(n log n)
- Sorting: O(n log n) - happens once
- Binary search: O(log n) iterations × O(n) per simulation = O(n log n)
- Total: O(n log n) + O(n log n) = O(n log n)

**Space Complexity**: O(n) for sorted array and deque

**Key Insight**: Since tasks are processed in sorted order and we always pick the earliest available CPU, the deque naturally maintains sorted order - allowing O(1) operations instead of O(log n) heap operations.

---

### Algorithm (sol2) - Backward with Max Heap
Uses backward processing with max heap (no binary search needed):
- code: [sol2.py](sol2.py)

1. **Sort start times** in increasing order
2. **Process backwards**: From last task to first
3. **Track free time boundaries**: Max heap stores the latest time each CPU can start a new task
4. **Greedy selection**: Always try to use CPU with largest free time boundary
5. **Update rule**: When task fits, move free boundary earlier by `task_length`

**Time Complexity**: O(n log n)
- Sorting: O(n log n)
- Heap operations: O(log k) per task where k = CPU count ≤ n
- Total: O(n log n) + O(n log n) = O(n log n)

**Space Complexity**: O(k) for max heap, where k ≤ n

**Key Insight**: Working backwards from the deadline allows direct minimization without binary search. The max heap greedily selects the CPU with most free time, ensuring optimal packing towards the end time.

---

## Test Cases
- code: [test_cases.py](test_cases.py)

8 test cases covering:
- Edge cases (single task, empty input)
- No overlap scenarios (tasks can run sequentially)
- Full overlap scenarios (all tasks start together)
- Partial overlap scenarios
- Large scale test (50 tasks with grouped start times)

---

## How to Run

### Run tests with default solution (sol1):
```bash
python3 main.py
```

### Run tests with specific solution:
```bash
python3 main.py sol1  # Forward with binary search
python3 main.py sol2  # Backward with max heap
```

### Project Structure:
```
min_cpu_run_task/
├── README.md          # This file
├── sol1.py            # Forward approach with binary search
├── sol2.py            # Backward approach with max heap
├── test_cases.py      # Shared test cases
├── main.py            # Test runner
├── Main.java          # Java version (TreeMap approach)
└── MainMaxHeap.java   # Java version (Max heap approach)
```

### Expected Output:
```
Running tests for sol1...

✓ Test 1 (example1_large_gap): got 1, expected 1
✓ Test 2 (example2_all_same_start): got 3, expected 3
...
============================================================
Results: 8 passed, 0 failed out of 8 tests
============================================================
```
