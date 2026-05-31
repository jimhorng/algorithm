from __future__ import annotations


class Solution:
    def line_count(self, s: str, doc_width: int) -> int:
        if doc_width <= 0:
            raise ValueError("doc_width must be positive")

        line_count = 0
        line_len = 0
        index = 0

        while index < len(s):
            if not s[index].isalpha():
                line_len += 1
                index += 1

                if line_len == doc_width:
                    line_count += 1
                    line_len = 0

                continue

            word_start = index
            while index < len(s) and s[index].isalpha():
                index += 1

            word_len = index - word_start

            if word_len <= doc_width:
                if line_len + word_len > doc_width:
                    line_count += 1
                    line_len = 0

                line_len += word_len
                if line_len == doc_width:
                    line_count += 1
                    line_len = 0

                continue

            if line_len > 0:
                line_count += 1
                line_len = 0

            full_lines, line_len = divmod(word_len, doc_width)
            line_count += full_lines

        if line_len > 0:
            line_count += 1

        return line_count


if __name__ == "__main__":
    from test_cases import run_cases

    run_cases(Solution())
