1) recursion tree (top->down = left->right)
```
m = unique colors
n = grid size

     3^m path <= 3^m*m steps                            n-m steps               =>  < 3^m*n
/----------------------------------------\  /-----------------------------\
(0,0):0 -d1- (0,1):1 -d1- (0,2):2 -dx- ... (r,c):0 -d1- (r,c):1 -d1- ... ():-1
                     -d2- (1,1):3
                     -d3- ()   :4
        -d2- (1,0):1 -d1- ()      ..
                     -d2- ()      ..
                     -d3- ()      ..
        -d3- ()      -d1- ()      ..
                     -d2- ()      ..
                     -d3- ()      ..
```

2) since 3^m path's steps might overlap, so total step <= 3^m*m
3) if complete tree at first m step, easier to calculate
```
m=2, 3^m*m = 18, actual = 13
s1 - s2 - s5 
        - s6 
        - s7
   - s3 - s8
        - s9
        - s10
   - s4 - s11
        - s12
        - s13
```
