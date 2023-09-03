1) infinite example:
```
V: cur A[i], *: cur idx, X: N/A

case 1: infinite
D=2, S=1, N=2, A=[2,1]

 0 1
[2,1]  V  dir
  <*   1   <
 *>3   2   >
 4<*   3   <
 ..

case 2: not infinite
D=3, S=1, N=3, A=[2,1,3]

 0 1 2
[2,1,3]  V  dir
  <*     1  <
 *>4     2  >
 5  <*   3  <
   *>6   4  >
  X      5

case 3: infinite
D=4, S=2, N=4, A=[2,4,1,3]

 0 1 2 3
[2,4,1,3]  V  dir
    <*     1  <
 *>  5     2  >
 6    <*   3  <
   *>  7   4  >
   8<*     5  <
 *>  9     6  >
 ..
```

2) loop same set of 4 idxs
```
idx: 2 -> 0 -> 3 -> 1 -> 2 -> 0 -> 3 -> 1 -> ..
     ^    ^    ^    ^    
```

3) when size of idxes in loop equals D, all A[i] are unique
  4) verify by run D+2 to check if cur idx still valid, if so, it's inf

5) how about A contains dup in some state?
```
case 4: not infinite
D=3, S=1, N=5, A=[2,1,3,1,5]

 0 1 2 3 4
[2,1,3,1,5]  V  dir
  <*   x     1  <
 *>4         2  >
 5  <*       3  <
   *>6       4  >
 x 7    <*   5  <
     *>  8   6  >
      X      7  <
```

6) A[i] <= V will no longer needed (mark as x), only 1 A[i] = V will remain

7) when V=N+1, remain size of A <= D, since only when A[i] >= N-D+1 can exceed N, at most D unique
e.g.
```
case 5:
D=3, S=1, N=5, A=[2,1,3,1,5]

 0 1 2 3 4
[2,1,3,1,5]  V  dir  N-D+1=3 (val:[idxes])
  <*   x     1  <     3:[2], 5:[4]
 *>4         2  >     3:[2], 4:[1], 5:[4]
 5  <*       3  <     3:[2], 4:[1], 5:[0,4]
   *>6       4  >     4:[1], 5:[0,4]       | 6:[2]
 x 7    <*   5  <     5:[4]                | 6:[2], 7:[1]
--------------------
     *>  8   6  >                          | 6:[2], 7:[1], 8:[4]
      X      7  <
```

8) sum-up, run operation till V=N+1 (6,7), and run additional D+2 (4) to verify if inf

### code
```python3
def q(A, S, D):
    LEFT, RIGHT = 0, 1
    INF = -1
    MAX, MIN = sys.maxsize, -sys.maxsize
    n = len(A)
    
    val_idxes = {} # val:[idxes]
    for i in range(n):
        if A[i] < A[S]: continue
        if A[i] not in val_idxes:
            val_idxes[A[i]] = set()
        val_idxes[A[i]].add(i)
    cur_idx = S
    dirn = LEFT
    for val in range(A[S], n+D+2+1):
        val_nx = val+1
        idx_cands = val_idxes[val_nx]
        next_cur_idx = None
        if dirn == LEFT:
            idx_left = MIN
            for idx in idx_cands:
                if idx < cur_idx:
                    idx_left = max(idx_left, idx)
            next_cur_idx = idx_left
        elif dirn == RIGHT:
            idx_right = MAX
            for idx in idx_cands:
                if idx > cur_idx:
                    idx_right = min(idx_right, idx)
            next_cur_idx = idx_right
        if next_cur_idx in (MIN, MAX):
            return cur_idx
        # update +D to cur_idx, del org val
        del val_idxes[val]
        if val+D not in val_idxes:
            val_idxes[val+D] = set()
        val_idxes[val+D].add(cur_idx)
        cur_idx = next_cur_idx
        dirn = RIGHT if dirn == LEFT else LEFT
        
    return INF

```
* test case
```python3
testcases = [
    {
        "id": 1,
        "input": {
            "A": [2, 4, 3, 5, 1, 2],
            "S": 4,
            "D": 3,
        },
        "output": 2,
    },
    {
        "id": 2,
        "input": {
            "A": [2,1],
            "S": 1,
            "D": 2,
        },
        "output": -1,
    },
    {
        "id": 3,
        "input": {
            "A": [2,1,3],
            "S": 1,
            "D": 3,
        },
        "output": 1,
    },
    {
        "id": 4,
        "input": {
            "A": [2,4,1,3],
            "S": 2,
            "D": 4,
        },
        "output": -1,
    },
    {
        "id": 5,
        "input": {
            "A": [2,1,3,1,5],
            "S": 1,
            "D": 3,
        },
        "output": 2,
    },
]
for tc in testcases:
    output = q(**tc["input"])
    print(f"""case {tc["id"]}: {tc["output"] == output}, output:{output}""")
```
