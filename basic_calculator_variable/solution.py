class Solution:
    def simplify(self, expression: str) -> str:
        counts = [0] * 26
        order: list[int] = []
        seen = [False] * 26

        stack = [1]
        current_sign = 1

        for ch in expression:
            if ch == " ":
                continue
            if ch == "+":
                current_sign = 1
                continue
            if ch == "-":
                current_sign = -1
                continue
            if ch == "(":
                stack.append(stack[-1] * current_sign)
                current_sign = 1
                continue
            if ch == ")":
                stack.pop()
                current_sign = 1
                continue

            idx = ord(ch) - ord("a")
            if 0 <= idx < 26:
                if not seen[idx]:
                    seen[idx] = True
                    order.append(idx)
                counts[idx] += stack[-1] * current_sign
                current_sign = 1
                continue

            raise ValueError(f"Unsupported character: {ch!r}")

        parts: list[str] = []
        for idx in order:
            coefficient = counts[idx]
            if coefficient == 0:
                continue

            variable = chr(ord("a") + idx)
            sign = "+" if coefficient > 0 else "-"
            absolute = abs(coefficient)

            if absolute == 1:
                term = variable
            else:
                term = f"{absolute}{variable}"

            if not parts:
                parts.append(term if sign == "+" else f"-{term}")
            else:
                parts.append(f"{sign}{term}")

        return "".join(parts)


def main() -> None:
    from test_cases import run_cases

    run_cases(Solution())


if __name__ == "__main__":
    main()
