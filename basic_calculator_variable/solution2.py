from collections import defaultdict


class Solution:
    def simplify(self, expression: str) -> str:
        INVERT, NON_INVERT = 1, 0
        # clean
        s = [c for c in expression if c.strip()]
        invert = {} # {critical point: invert_count}
        lp_stack = [] # idx of s
        
        # record invert points
        for i in range(len(s)):
            if s[i] == '(':
                if i-1 >= 0 and s[i-1] == '-':
                    lp_stack.append((i, INVERT))
                else:
                    lp_stack.append((i, NON_INVERT))
            if s[i] == ')':
                i_lp, invert_type = lp_stack.pop()
                i_rp = i
                if invert_type == INVERT:
                    invert[i_lp] = invert.get(i_lp, 0) + 1
                    invert[i_rp] = invert.get(i_rp, 0) - 1

        si = [] # s_inverted
        invert_cur = 0
        for i in range(len(s)):
            c = s[i]
            if invert.get(i) != None:
                invert_cur = (invert_cur + invert[i]) % 2
            if c in '()':
                continue
            elif c in '+-':
                if invert_cur == INVERT:
                    c = '+' if c == '-' else '-'
            si.append(c)
        
        # char freq
        char_count = defaultdict(int)
        for i in range(len(si)):
            c = si[i]
            if c in '+-':
                continue
            if i == 0 or si[i-1] == '+':
                char_count[c] += 1
            else:
                char_count[c] -= 1

        print(f"char_count: {char_count}")

        final = []
        for c, cnt in char_count.items():
            if cnt == 0:
                continue
            if cnt > 0:
                final.append('+')
            elif cnt < 0:
                final.append('-')
                cnt = abs(cnt)
            if cnt > 1 or cnt < -1: # count not 1
                final.append(str(cnt))
            final.append(c)
            
        return "".join(final[1:])


def main() -> None:
    from test_cases import run_cases

    run_cases(Solution())


if __name__ == "__main__":
    main()
