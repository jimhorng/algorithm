from __future__ import annotations


class Solution:
    def simplify(self, expression: str) -> str:
        compact_chars = self._remove_spaces(expression)
        flip_deltas = self._collect_flip_deltas(compact_chars)
        flattened_chars = self._flatten_expression(compact_chars, flip_deltas)
        variable_counts = self._count_variables(flattened_chars)
        return self._build_result(variable_counts)

    def _remove_spaces(self, expression: str) -> list[str]:
        return [ch for ch in expression if ch != " "]

    def _collect_flip_deltas(self, chars: list[str]) -> list[int]:
        flip_deltas = [0] * (len(chars) + 1)
        parentheses_stack: list[tuple[int, bool]] = []

        for index, ch in enumerate(chars):
            if ch == "(":
                should_flip_inside = index > 0 and chars[index - 1] == "-"
                parentheses_stack.append((index, should_flip_inside))
                continue

            if ch == ")":
                left_index, should_flip_inside = parentheses_stack.pop()
                if should_flip_inside:
                    flip_deltas[left_index + 1] += 1
                    flip_deltas[index] -= 1

        return flip_deltas

    def _flatten_expression(self, chars: list[str], flip_deltas: list[int]) -> list[str]:
        flattened_chars: list[str] = []
        active_flip = 0

        for index, ch in enumerate(chars):
            active_flip = (active_flip + flip_deltas[index]) % 2

            if ch in "()":
                continue

            if ch in "+-" and active_flip == 1:
                ch = "+" if ch == "-" else "-"

            flattened_chars.append(ch)

        return flattened_chars

    def _count_variables(self, flattened_chars: list[str]) -> dict[str, int]:
        counts: dict[str, int] = {}
        next_sign = 1

        for ch in flattened_chars:
            if ch == "+":
                next_sign = 1
                continue

            if ch == "-":
                next_sign = -1
                continue

            counts.setdefault(ch, 0)
            counts[ch] += next_sign
            next_sign = 1

        return counts

    def _format_term(self, variable_name: str, coefficient: int) -> str:
        absolute_value = abs(coefficient)
        if absolute_value == 1:
            return variable_name
        return f"{absolute_value}{variable_name}"

    def _build_result(self, variable_counts: dict[str, int]) -> str:
        parts: list[str] = []

        for variable_name, coefficient in variable_counts.items():
            if coefficient == 0:
                continue

            term = self._format_term(variable_name, coefficient)
            if not parts:
                parts.append(term if coefficient > 0 else f"-{term}")
                continue

            parts.append(f"+{term}" if coefficient > 0 else f"-{term}")

        return "".join(parts)

if __name__ == "__main__":
    from test_cases import run_cases

    run_cases(Solution())
