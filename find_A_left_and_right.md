```
1) infinite example:

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

2) idx: 2 -> 0 -> 3 -> 1 -> 2 -> 0 -> 3 -> 1 -> ..
        ^    ^    ^    ^    loop same 4 idxs
3) when size of idxes in loop equals D, all A[i] are unique
  4) verify by run D+2 to check if cur idx still valid
5) how about A contains dup in some state?
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

6) A[i] <= V will no longer needed (mark as x), only 1 A[i] = V will remain

7) when V=N+1, remain size of A <= D, since only when A[i] >= N-D+1 can exceed N, at most D unique
e.g.
D=3, S=1, N=5, A=[2,1,3,1,5]

 0 1 2 3 4
[2,1,3,1,5]  V  dir  N-D+1=3 (val:idxes)
  <*   x     1  <     3:[2], 5:[4]
 *>4         2  >     3:[2], 4:[1], 5:[4]
 5  <*       3  <     3:[2], 4:[1], 5:[0,4]
   *>6       4  >     4:[1], 5:[0,4]       | 6:[2]
 x 7    <*   5  <     5:[4]                | 6:[2], 7:[1]
--------------------
     *>  8   6  >                          | 6:[2], 7:[1], 8:[4]
      X      7  <

8) sum-up, run operation till V=N+1 (6,7), and run additional D+2 (3), all non-inf will stop, all inf will still have cur idx
```
