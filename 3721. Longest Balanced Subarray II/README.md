# Longest Balanced Subarray II

Given `nums`, return the length of the longest subarray where the number of
distinct even values equals the number of distinct odd values.

## Step-by-Step Segment Tree Reasoning

1. Start with the simpler prefix idea.
   If each distinct odd value contributes `+1` and each distinct even value
   contributes `-1`, then a subarray is balanced when its net contribution is
   `0`.

2. The hard part is "distinct".
   A repeated value should only contribute once inside a subarray. So we cannot
   just add `+1` or `-1` for every occurrence.

3. Store each value at its latest occurrence.
   While scanning left to right, imagine a prefix array `score[k]`: the net
   odd/even contribution of distinct values whose latest occurrence is at or
   before prefix index `k`.

4. Move a repeated value's contribution.
   When value `x` appears at position `i`, its contribution belongs at `i`.
   If `x` appeared before at `prev`, remove its old contribution from all
   prefixes `prev..n`, then add the new contribution to all prefixes `i..n`.

5. Why range add?
   Adding a contribution at position `i` changes every later prefix. That is a
   range update, so a lazy segment tree is a natural fit.

6. Find the earliest matching prefix.
   Let `current` be the current net contribution after processing `nums[:i]`.
   A subarray ending at `i` is balanced when an earlier prefix has the same
   score. The longest one uses the earliest prefix with `score == current`.

7. Why store min and max in each tree node?
   Prefix scores change by `+1` or `-1`, so within a segment, if `target` lies
   between the node's minimum and maximum score, some position in that segment
   can contain `target`. Search left first to get the earliest index.

## Example

For `nums = [2, 5, 4, 3]`, use `-1` for even and `+1` for odd.

```text
i=1, x=2: current=-1, earliest same score gives length 0
i=2, x=5: current=0,  earliest same score is 0, length 2
i=3, x=4: current=-1, earliest same score gives length 2
i=4, x=3: current=0,  earliest same score is 0, length 4
```

Answer: `4`.

## Complexity

- Each occurrence performs at most two range updates and one search.
- Time: `O(n log n)`
- Space: `O(n)`

## Run

```bash
python3 '3721. Longest Balanced Subarray II/solution_segtree.py'
```
