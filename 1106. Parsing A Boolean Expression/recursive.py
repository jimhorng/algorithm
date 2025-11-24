class Solution:
    BOOLS = ("t", "f")
    OPERATORS = ("|", "&", "!")

    def parseBoolExpr(self, expression: str) -> bool:
        # no operator
        if expression[0] in self.BOOLS:
            return self._convert(expression[0])
        return self._f(0, expression)[0]

    def _convert(self, char):
        return True if char == 't' else False

    def _calc(self, operator, bools):
        if operator == '|':
            return any(bools)
        elif operator == '&':
            return all(bools)
        elif operator == '!':
            return not bools[0]

    def _f(self, start, expr):
        """ ret: result bool, last idx """
        cur = start
        operator = expr[cur]
        cur += 2 # skip operator, (
        bools = []
        while expr[cur] != ')':
            if expr[cur] in self.BOOLS:
                bools.append(self._convert(expr[cur]))
            elif expr[cur] == ',':
                pass
            elif expr[cur] in self.OPERATORS:
                bool_val, cur = self._f(cur, expr)
                bools.append(bool_val)
            cur += 1
        bool_val = self._calc(operator, bools)
        return bool_val, cur
