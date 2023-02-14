# Sliding Window
### template 1
```python
find_1st_window()
process_state()
while not is_reach_end():
    move_1_end()
    move_another_end_till_condition()
    process_state()
return result
```
### template 2
```python
init()
while not is_reach_end():
    move_one_end()
    move_another_end_till_invalid()
    process_state()
return result
```

### [567. Permutation in String]([url](https://leetcode.com/problems/permutation-in-string/))
#### template 1
```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n1, n2 = len(s1), len(s2)

        def get_char_cnt(s):
            char_cnt = defaultdict(int)
            for c in s:
                char_cnt[c] += 1
            return char_cnt
        
        def char_cnt_enough(s1_char_cnt, s2_char_cnt):
            for c, cnt in s1_char_cnt.items():
                if s2_char_cnt[c] < cnt:
                    return False
            return True

        def find_1st_window():
            self.l_win, self.r_win = 0, 0
            self.s2_win_char_cnt = defaultdict(int)
            for r_win in range(n2):
                self.r_win = r_win
                self.s2_win_char_cnt[s2[self.r_win]] += 1
                if char_cnt_enough(self.s1_char_cnt, self.s2_win_char_cnt):
                    move_another_end_till_condition()
                    return

        def process_state():
            # s1 and s2's window has same char cnt and size
            return (char_cnt_enough(self.s1_char_cnt, self.s2_win_char_cnt)
                    and n1 == self.r_win - self.l_win + 1)

        def is_reach_end():
            return self.r_win >= n2-1

        def move_1_end():
            self.r_win += 1
            self.s2_win_char_cnt[s2[self.r_win]] += 1

        def move_another_end_till_condition():
            while True:
                # try move left
                self.s2_win_char_cnt[s2[self.l_win]] -= 1
                self.l_win += 1
                if not char_cnt_enough(self.s1_char_cnt, self.s2_win_char_cnt):
                    # add back
                    self.s2_win_char_cnt[s2[self.l_win-1]] += 1
                    self.l_win -= 1
                    break

        # main
        self.s1_char_cnt = get_char_cnt(s1)
        find_1st_window()
        found = process_state()
        if found:
            return True
        while not is_reach_end():
            move_1_end()
            move_another_end_till_condition()
            found = process_state()
            if found:
                return True
        return False
```
#### template 2
```python
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        n1, n2 = len(s1), len(s2)

        def get_char_cnt(s):
            char_cnt = defaultdict(int)
            for c in s:
                char_cnt[c] += 1
            return char_cnt
        
        def char_cnt_enough(s1_char_cnt, s2_char_cnt):
            for c, cnt in s1_char_cnt.items():
                if s2_char_cnt[c] < cnt:
                    return False
            return True

        def init():
            self.s1_char_cnt = get_char_cnt(s1)
            self.l_win, self.r_win = 0, -1
            self.s2_win_char_cnt = defaultdict(int)

        def process_state():
            # s1 and s2's window has same char cnt and size
            return (char_cnt_enough(self.s1_char_cnt, self.s2_win_char_cnt)
                    and n1 == self.r_win - self.l_win + 1)

        def is_reach_end():
            return self.r_win >= n2-1

        def move_one_end():
            self.r_win += 1
            self.s2_win_char_cnt[s2[self.r_win]] += 1

        def move_another_end_till_invalid():
            moved = False
            while char_cnt_enough(self.s1_char_cnt, self.s2_win_char_cnt):
                self.s2_win_char_cnt[s2[self.l_win]] -= 1
                self.l_win += 1
                moved = True
            if moved:
                # add back
                self.s2_win_char_cnt[s2[self.l_win-1]] += 1
                self.l_win -= 1

        # main
        init()
        while not is_reach_end():
            move_one_end()
            move_another_end_till_invalid()
            found = process_state()
            if found: return True
        return False
```

### [1838. Frequency of the Most Frequent Element]([url](https://leetcode.com/problems/frequency-of-the-most-frequent-element/))
#### template 1
```python
class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def find_1st_window():
            self.l_win, self.r_win = 0, 0
            self.k_used = 0

        def process_state():
            self.k_most = max(self.k_most, self.r_win-self.l_win+1)

        def is_reach_end():
            return self.r_win >= n-1

        def move_1_end():
            self.r_win += 1
            self.k_used += (self.nums_st[self.r_win]-self.nums_st[self.r_win-1]) * (self.r_win-1 - self.l_win + 1)

        def move_another_end_till_condition():
            while self.k_used > k:
                self.k_used -= (self.nums_st[self.r_win]-self.nums_st[self.l_win])
                self.l_win += 1

        # main
        self.nums_st = sorted(nums)
        self.k_most = 1
        find_1st_window()
        process_state()
        while not is_reach_end():
            move_1_end()
            move_another_end_till_condition()
            process_state()
        return self.k_most
```
#### template 2
```python
class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def init():
            self.nums_st = sorted(nums)
            self.k_most = 1
            self.l_win, self.r_win = 0, 0
            self.k_used = 0

        def process_state():
            self.k_most = max(self.k_most, self.r_win-self.l_win+1)

        def is_reach_end():
            return self.r_win >= n-1

        def move_one_end():
            self.r_win += 1
            self.k_used += (self.nums_st[self.r_win]-self.nums_st[self.r_win-1]) * (self.r_win-1 - self.l_win + 1)

        def move_another_end_till_invalid():
            while self.k_used > k:
                self.k_used -= (self.nums_st[self.r_win]-self.nums_st[self.l_win])
                self.l_win += 1

        # main
        init()
        while not is_reach_end():
            move_one_end()
            move_another_end_till_invalid()
            process_state()
        return self.k_most
```

### [1888. Minimum Number of Flips to Make the Binary String Alternating]([url](https://leetcode.com/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/description/))
#### template 1
```python
class Solution:
    def minFlips(self, s: str) -> int:
        MAX = sys.maxsize
        n = len(s)
        n_half_lg, n_half_sm = math.ceil(n/2), math.floor(n/2)

        def find_1st_window():
            self.even_1s, self.odd_1s, self.even_0s, self.odd_0s = 0, 0, 0, 0
            for i in range(n):
                if i % 2 == 0:
                    if s[i] == '1': self.even_1s += 1
                    else: self.even_0s += 1
                elif i % 2 == 1:
                    if s[i] == '1': self.odd_1s += 1
                    else: self.odd_0s += 1
            self.l_win, self.r_win = 0, n-1

        def process_state():
            flips_needed = min(n_half_lg - max(self.even_1s, self.odd_0s) + n_half_sm - min(self.even_1s, self.odd_0s),
                               n_half_lg - max(self.even_0s, self.odd_1s) + n_half_sm - min(self.even_0s, self.odd_1s))
            self.res = min(self.res, flips_needed)

        def is_reach_end():
            return self.l_win > n-1

        def move_1_end():
            self.r_win = self.r_win+1 if self.r_win < n-1 else 0
            self.even_1s, self.odd_0s, self.even_0s, self.odd_1s = self.odd_1s, self.even_0s, self.odd_0s, self.even_1s
            if n % 2 == 0:
                if s[self.r_win] == '1': self.odd_1s += 1
                else: self.odd_0s += 1
            elif n % 2 == 1:
                if s[self.r_win] == '1': self.even_1s += 1
                else: self.even_0s += 1

        def move_another_end_till_condition():
            if s[self.l_win] == '1': self.odd_1s -= 1
            else: self.odd_0s -= 1
            self.l_win += 1

        # main
        self.res = MAX
        find_1st_window()
        process_state()
        while not is_reach_end():
            move_1_end()
            move_another_end_till_condition()
            process_state()
        return self.res
```
#### template 2
```python
class Solution:
    def minFlips(self, s: str) -> int:
        MAX = sys.maxsize
        n = len(s)
        n_half_lg, n_half_sm = math.ceil(n/2), math.floor(n/2)

        def is_r_win_even():
            return self.sz_win % 2 == 0

        def init():
            self.res = MAX
            self.even_1s, self.odd_1s, self.even_0s, self.odd_0s = 0, 0, 0, 0
            self.l_win, self.r_win = 0, -1
            self.sz_win = 0

        def process_state():
            flips_needed = min(n_half_lg - max(self.even_1s, self.odd_0s) + n_half_sm - min(self.even_1s, self.odd_0s),
                               n_half_lg - max(self.even_0s, self.odd_1s) + n_half_sm - min(self.even_0s, self.odd_1s))
            self.res = min(self.res, flips_needed)

        def is_reach_end():
            return self.l_win > n-1

        def move_one_end():
            self.r_win = (self.r_win+1) % n
            self.sz_win += 1
            if is_r_win_even():
                if s[self.r_win] == '1': self.even_1s += 1
                elif s[self.r_win] == '0': self.even_0s += 1
            else:
                if s[self.r_win] == '1': self.odd_1s += 1
                elif s[self.r_win] == '0': self.odd_0s += 1
                

        def move_another_end_till_invalid():
            if self.sz_win > n:
                if s[self.l_win] == '1': self.odd_1s -= 1
                elif s[self.l_win] == '0': self.odd_0s -= 1
                self.even_1s, self.odd_0s, self.even_0s, self.odd_1s = self.odd_1s, self.even_0s, self.odd_0s, self.even_1s
                self.l_win += 1
                self.sz_win -= 1

        # main
        init()
        while not is_reach_end():
            move_one_end()
            move_another_end_till_invalid()
            process_state()
        return self.res
```
