# Basic Calculator With Variables

Given an expression containing:

- lowercase variables `a` to `z`
- operators `+` and `-`
- parentheses `(` and `)`
- optional spaces

simplify the expression by combining like terms.

## Rules

- Remove spaces.
- Apply the signs implied by parentheses.
- Combine the coefficient of the same variable.
- If a variable coefficient becomes `0`, remove it.
- Variables are limited to `26` lowercase letters.

## Examples

### Example 1

Input:

```text
"a + b"
```

Output:

```text
"a+b"
```

### Example 2

Input:

```text
"a + a"
```

Output:

```text
"2a"
```

### Example 3

Input:

```text
"a-(b+c-(d-e))"
```

Output:

```text
"a-b-c+d-e"
```

### Example 4

Input:

```text
"a-a"
```

Output:

```text
""
```

### Example 5

Input:

```text
"b + a + b + a"
```

Output:

```text
"2b+2a"
```

## Goal

Convert the input expression into a canonical simplified form.

For each variable:

- keep a signed count
- merge repeated variables into a coefficient
- omit coefficient `1` in the output, so `1a` becomes `a`
- use `-` for negative terms and `+` between positive terms

## Solution 1

Use a stack of signs while scanning the string from left to right.

### Idea

- Maintain a current sign context caused by nested parentheses.
- For each variable, compute its final sign after considering:
  - the local operator before it
  - the active sign context from outer parentheses
- Accumulate the result in a size-26 counter array.

### Steps

1. Remove spaces, or skip them while scanning.
2. Use a stack to track the sign contributed by each parenthesis level.
3. Keep a `currentSign` for the operator immediately before the next variable or `(`.
4. When seeing `(`:
   - push `stackTop * currentSign`
5. When seeing `)`:
   - pop the stack
6. When seeing a variable `ch`:
   - add `stackTop * currentSign` to `count[ch]`
7. When seeing `+`, set `currentSign = +1`
8. When seeing `-`, set `currentSign = -1`
9. Build the result string from the accumulated counts.

## Output Construction

For each variable with non-zero count:

- `1` becomes `a`
- `2` becomes `2a`
- `-1` becomes `-a`
- `-2` becomes `-2a`

If no variable remains, return an empty string.

## Complexity

- Time: `O(n)`
- Space: `O(n)` for the parentheses stack, plus `O(26)` for counts

## Notes

- The sample output order follows the first appearance style shown in the examples, such as `2b+2a`.
- If strict output ordering is required, define it explicitly:
  - alphabetical order
  - first appearance order

Without that rule, multiple simplified strings may be equivalent.
