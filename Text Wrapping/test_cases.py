from __future__ import annotations


TEST_CASES = [
    {
        "name": "fits on one line",
        "s": "hello world",
        "doc_width": 20,
        "expected": 1,
    },
    {
        "name": "space counts exactly at width",
        "s": "hello world",
        "doc_width": 11,
        "expected": 1,
    },
    {
        "name": "word moves when separating space would overflow",
        "s": "hello world",
        "doc_width": 10,
        "expected": 2,
    },
    {
        "name": "repeated spaces are preserved and counted",
        "s": "a  bc d",
        "doc_width": 4,
        "expected": 2,
    },
    {
        "name": "leading spaces are preserved",
        "s": "  a",
        "doc_width": 3,
        "expected": 1,
    },
    {
        "name": "trailing spaces are preserved",
        "s": "a  ",
        "doc_width": 3,
        "expected": 1,
    },
    {
        "name": "repeated spaces may fill the rest of a line",
        "s": "a   b",
        "doc_width": 4,
        "expected": 2,
    },
    {
        "name": "single overlong word splits into chunks",
        "s": "understand",
        "doc_width": 6,
        "expected": 2,
    },
    {
        "name": "overlong word chunk starts on a new line",
        "s": "ab understand cd",
        "doc_width": 6,
        "expected": 4,
    },
    {
        "name": "empty string has no output lines",
        "s": "",
        "doc_width": 5,
        "expected": 0,
    },
    {
        "name": "multiple symbols",
        "s": " ,,,  .,.",
        "doc_width": 3,
        "expected": 3,
    },
]


def run_cases(solution) -> None:
    for index, case in enumerate(TEST_CASES, start=1):
        actual = solution.line_count(case["s"], case["doc_width"])
        assert actual == case["expected"], (
            f"Case {index} failed: {case['name']}; "
            f"s={case['s']!r}, doc_width={case['doc_width']!r}, "
            f"expected={case['expected']!r}, got={actual!r}"
        )

    print(f"Passed {len(TEST_CASES)} test cases.")
