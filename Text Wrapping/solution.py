class Solution:
    def line_count(self, s: str, doc_width: int) -> int:
        """Return the number of lines after wrapping s to doc_width."""
        n = len(s)

        output = 0
        word_cur_len = 0
        line_cur_len = 0
        for i, c in enumerate(s):
            if c.isalpha():
                word_cur_len += 1
                is_word_end = (i == n-1) or (not s[i+1].isalpha())
                if is_word_end:
                    line_cur_len += word_cur_len
                    word_cur_len = 0
            else:
                line_cur_len += 1
            if ((line_cur_len + word_cur_len == doc_width) 
                or i == n-1): # remaining
                output += 1
                line_cur_len = 0
                # long word and truncate
                if word_cur_len == doc_width and not is_word_end:
                    word_cur_len = 0

        return output


if __name__ == "__main__":
    from test_cases import run_cases

    run_cases(Solution())
