class Solution:
    def parseBoolExpr(self, expression: str) -> bool:
        BOOLS = ("t", "f")
        OPERATORS = ("|", "&", "!")

        def _calc(operator, bools):
            if operator == '|':
                return any(bools)
            elif operator == '&':
                return all(bools)
            elif operator == '!':
                return not bools[0]

        def _f(start):
            """ ret: result bool, next idx """
            cur = start
            operator = expression[cur]
            cur += 2 # skip operator, (
            bools = []
            while expression[cur] != ')':
                if expression[cur] in BOOLS:
                    bools.append(True if expression[cur] == 't' else False)
                elif expression[cur] == ',':
                    pass
                elif expression[cur] in OPERATORS:
                    bool_val, cur = _f(cur)
                    bools.append(bool_val)
                cur += 1
            bool_val = _calc(operator, bools)
            return bool_val, cur

        # no operator
        if expression[0] in BOOLS:
            return True if expression[0] == 't' else False
        return _f(0)[0]
