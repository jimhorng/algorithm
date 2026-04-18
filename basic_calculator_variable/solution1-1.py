from collections import defaultdict


class Solution:
    def simplify(self, expression: str) -> str:
        flattened_chars = self._flatten_expression(expression)
        variable_counts = self._count_variables(flattened_chars)
        return self._build_result(variable_counts)

    def _flatten_expression(self, chars: str) -> list[str]:
        flattened_chars: list[str] = []
        flips = [0] # 0: non-flip, 1: flip, stack top is latest
        for c in chars:
            if c == " ":
                continue
            if c == "(":
                if not flattened_chars or flattened_chars[-1] == "+":
                    flips.append(0)
                elif flattened_chars[-1] == "-":
                    flips.append(1)
                continue
            if c == ")":
                flips.pop()
                continue
            # flip sign
            if c in "+-" and flips[-1] == 1:
                c = "+" if c == "-" else "-"
            flattened_chars.append(c)
        return flattened_chars

    def _count_variables(self, flattened_chars: list[str]) -> dict[str, int]:
        counts = defaultdict(int)
        for i in range(len(flattened_chars)):
            c, c_prev = flattened_chars[i], flattened_chars[i-1] if i-1 >=0 else None
            if c in "+-":
                continue
            if c_prev in ("+", None):
                counts[c] += 1
            elif c_prev == "-":
                counts[c] -= 1
        return counts

    def _format_term(self, variable_name: str, coefficient: int) -> str:
        coef = abs(coefficient) if abs(coefficient) > 1 else ""
        return f"{coef}{variable_name}"

    def _build_result(self, variable_counts: dict[str, int]) -> str:
        parts: list[str] = []
        for variable_name, coefficient in variable_counts.items():
            if coefficient == 0:
                continue
            term = self._format_term(variable_name, coefficient)
            if not parts and coefficient > 0:
                parts.append(f"{term}")
            else:
                parts.append(f"+{term}" if coefficient > 0 else f"-{term}")
        return "".join(parts)

if __name__ == "__main__":
    from test_cases import run_cases

    run_cases(Solution())
