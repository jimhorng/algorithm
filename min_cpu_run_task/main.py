"""
Unified test runner for all min-CPU problems.

Usage:
    python main.py prob=<problem>               # run one problem with all default solutions
    python main.py prob=<problem> sol=<module>  # run one problem with a specific solution module

    <problem> : 1 | 2 | 3 | 4
    <module>  : e.g. prob1_sol1, prob1_sol2, prob2_sol1, prob2_sol2, ...

Examples:
    python main.py prob=2
    python main.py prob=1 sol=prob1_sol2
    python main.py prob=2 sol=prob2_sol1
"""

import sys
import importlib

# ── Problem registry ────────────────────────────────────────────────────────
# arg_keys: keys extracted from each test-case dict and passed to the solution
#           in the listed order.
PROBLEM_CONFIG = {
    "1": {
        "test_module":      "prob1_test_cases",
        "test_list":        "prob1_test_cases",
        "default_solutions": ["prob1_sol1", "prob1_sol2", "prob1_sol3"],
        "arg_keys":         ["start_times", "task_length"],
    },
    "2": {
        "test_module":      "prob2_test_cases",
        "test_list":        "prob2_test_cases",
        "default_solutions": ["prob2_sol1", "prob2_sol2", "prob2_sol3", "prob2_sol4"],
        "arg_keys":         ["start_times", "task_lengths"],
    },
    "3": {
        "test_module":      "prob3_test_cases",
        "test_list":        "prob3_test_cases",
        "default_solutions": ["prob3_sol1", "prob3_sol2", "prob3_sol3"],
        "arg_keys":         ["start_times", "task_length", "deadlines"],
    },
    "4": {
        "test_module":      "prob4_test_cases",
        "test_list":        "prob4_test_cases",
        "default_solutions": [],           # TODO: add when implemented
        "arg_keys":         ["start_times", "task_lengths", "deadlines"],
    },
}


def load_solution(solution_name, problem_key):
    """
    Import a solution module and return its entry-point function.

    Canonical entrypoint is `prob{problem_key}` (e.g. prob1, prob2, prob3).
    """
    mod = importlib.import_module(solution_name)
    canonical_name = f"prob{problem_key}"
    return getattr(mod, canonical_name)


def load_test_cases(problem_key):
    """Load the test-case list for a given problem key."""
    cfg = PROBLEM_CONFIG[problem_key]
    mod = importlib.import_module(cfg["test_module"])
    return getattr(mod, cfg["test_list"])


def run_tests(solution_func, test_cases, arg_keys, solution_name):
    """
    Run `test_cases` against `solution_func`.
    Args are extracted from each test-case dict using `arg_keys` (in order).
    Returns True if all tests pass.
    """
    passed = failed = 0
    print(f"Running tests for {solution_name}...\n")

    for i, tc in enumerate(test_cases):
        args = [tc[k] for k in arg_keys]
        result = solution_func(*args)
        ok = result == tc["expected"]
        passed += ok
        failed += not ok
        status = "✓" if ok else "✗"
        print(f"  {status} Test {i+1} ({tc['testcase']}): got {result}, expected {tc['expected']}")

    print(f"\n  {'='*56}")
    print(f"  Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print(f"  {'='*56}\n")
    return failed == 0


def run_problem(problem_key, solution_name=None):
    """
    Run tests for one problem.
    If solution_name is None, run all default solutions for that problem.
    Returns True if every tested solution passes.
    """
    cfg = PROBLEM_CONFIG[problem_key]
    solutions = [solution_name] if solution_name else cfg["default_solutions"]

    if not solutions:
        print(f"── Problem {problem_key}: no solutions implemented yet ──\n")
        return True

    try:
        test_cases = load_test_cases(problem_key)
    except (ImportError, AttributeError) as e:
        print(f"Error loading test cases for Problem {problem_key}: {e}\n")
        return False

    print(f"{'─'*60}")
    print(f"  Problem {problem_key}")
    print(f"{'─'*60}")

    all_passed = True
    for sol_name in solutions:
        try:
            func = load_solution(sol_name, problem_key)
        except (ImportError, AttributeError) as e:
            print(f"  Error loading solution '{sol_name}': {e}\n")
            all_passed = False
            continue
        all_passed &= run_tests(func, test_cases, cfg["arg_keys"], sol_name)

    return all_passed


def main():
    args = sys.argv[1:]

    if len(args) not in (1, 2):
        print(__doc__)
        sys.exit(1)

    if not args[0].startswith("prob="):
        print(f"First argument must be prob={{1..4}}, got '{args[0]}'.")
        print(__doc__)
        sys.exit(1)

    problem_key = args[0].split("=", 1)[1]
    if problem_key not in PROBLEM_CONFIG:
        print(f"Unknown problem '{problem_key}'. Choose from: {', '.join(sorted(PROBLEM_CONFIG))}.")
        sys.exit(1)

    if len(args) == 1:
        sys.exit(0 if run_problem(problem_key) else 1)

    if not args[1].startswith("sol="):
        print(f"Second argument must be sol=<solution_module>, got '{args[1]}'.")
        print(__doc__)
        sys.exit(1)

    solution_name = args[1].split("=", 1)[1]
    sys.exit(0 if run_problem(problem_key, solution_name) else 1)


if __name__ == "__main__":
    main()
