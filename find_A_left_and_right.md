1) infinite example:
```
V: cur A[i], *: cur idx

case 1:
D=2, S=1
A=[2,1]

 0 1
[2,1]  V  dir
  <*   1   <
 *>3   2   >
 4<*   3   <
 ..

case 2:
D=3, S=1
A=[2,1,3]

 0 1 2
[2,1,3]  V  dir
  <*     1  <
 *>4     2  >
 5  <*   3  <
   *>6   4  >
  X      5
```
