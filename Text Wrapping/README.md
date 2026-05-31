# Problem

Given an input string `s` and an integer `doc_width`, wrap `s` into a document
where every output line has width at most `doc_width`.

Return the total number of lines in the wrapped document.

## Wrapping Rules

1. Words should stay on the same line whenever they fit.
2. A word may not be split just to fill leftover space at the end of a line.
3. If a word is longer than `doc_width`, split that word into chunks of length
   at most `doc_width`.
4. Chunks produced from an overlong word must start on a new line.
5. Words are separated by one or more spaces.
6. Leading spaces, trailing spaces, and repeated spaces are part of the input and
   should not be ignored.
7. Spaces count toward `doc_width` when they appear on an output line.

Example:

```text
s = "understand"
doc_width = 6

wrapped document:
unders
tand

line_count = 2
```

Example with spaces:

```text
s = "a  bc d"
doc_width = 4

wrapped document:
a  b
c d

line_count = 2
```
