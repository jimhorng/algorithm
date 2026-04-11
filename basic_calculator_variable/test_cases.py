from __future__ import annotations


TEST_CASES = [
    ("a + b", "a+b"),
    ("a + a", "2a"),
    ("a-(b+c-(d-e))", "a-b-c+d-e"),
    ("a-a", ""),
    ("b + a + b + a", "2b+2a"),
    ("a-(a-b)", "b"),
    ("a-(b-(c-d))", "a-b+c-d"),
    ("x-(x-(x-x))", ""),
    ("z-(a-z)+a", "2z"),
    ("m-(n-(m+n-m))", "m"),
    ("a-(b-(c-(d-(e-(f-g+h)-i)+j)-k)+l)-m+n", "a-b+c-d+e-f+g-h-i-j-k-l-m+n"),
    ("a+b-c+d-(e-f+g-(h-i+j-(k-l)))+m-n+o-p+q-r+s-t+u-v+w-x+y-z", "a+b-c+d-e+f-g+h-i+j-k+l+m-n+o-p+q-r+s-t+u-v+w-x+y-z"),
    ("a-(b+c-d+(e-f-(g+h-(i-j+k-(l-m+n)))))+o-p", "a-b-c+d-e+f+g+h-i+j-k+l-m+n+o-p"),
    ("q-(w-(e-(r-(t-(y-(u-(i-(o-(p-a+b)-c)+d)-e)+f)-g)+h)-j)+k)-l", "q-w-r+t-y+u-i+o-p+a-b-c-d-f-g-h-j-k-l"),
    ("a+b+c+d+e-(a+b-(c-d+(e-f-(g-h+(i-j-(k-l+m-n))))))+o-p+q-r", "2c+2e-f-g+h-i+j+k-l+m-n+o-p+q-r"),
    ("z-(y-(x-(w-(v-(u-(t-(s-(r-(q-(p-(o-(n-(m-(l-(k-(j-(i-(h-(g-(f-(e-(d-(c-(b-a))))))))))))))))))))))))", "z-y+x-w+v-u+t-s+r-q+p-o+n-m+l-k+j-i+h-g+f-e+d-c+b-a"),
]


def run_cases(solution) -> None:
    for index, (expression, expected) in enumerate(TEST_CASES, start=1):
        actual = solution.simplify(expression)
        assert (
            actual == expected
        ), f"Case {index} failed: expression={expression!r}, expected={expected!r}, got={actual!r}"

    print(f"Passed {len(TEST_CASES)} test cases.")
