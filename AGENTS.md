# Repository Guidelines

## Project Structure & Module Organization

This repository is a collection of algorithm practice solutions. Most root-level files are standalone Python files named after the problem, for example `713. Subarray Product Less Than K.py`. Larger exercises live in `min_cpu_run_task/` and `basic_calculator_variable/`.

Problem directories usually contain variants (`prob2_sol1.py`, `solution2.py`), test files (`prob2_test_cases.py`, `test_cases.py`), and sometimes a local `README.md`. Java examples are under `min_cpu_run_task/`.

## Build, Test, and Development Commands

There is no project-wide build system. Use direct commands:

- `python3 path/to/solution.py` runs a standalone solution or local demo.
- `python3 basic_calculator_variable/solution2.py` shows the preferred self-contained run pattern with shared cases from `test_cases.py`.
- `python3 min_cpu_run_task/main.py` runs the scheduler exercise driver.
- `python3 min_cpu_run_task/prob1_test_cases.py` runs a specific test script.
- `javac min_cpu_run_task/MainMaxHeap.java && java -cp min_cpu_run_task MainMaxHeap` runs a Java example.

## Coding Style & Naming Conventions

Use Python 3, 4-space indentation, and clear function names that match the algorithm. Keep solution files self-contained unless a folder has shared helpers. Existing naming is problem-oriented: root files may include the LeetCode number and title, while folders use suffixes such as `sol1`, `sol2`, or names like `binary_search.py`.

Avoid broad refactors. If a solution is exploratory, document known failure cases in the local README or near the test data.

## Testing Guidelines

Tests are lightweight and problem-specific. Follow `basic_calculator_variable/`: keep each solution self-contained and directly runnable, but move shared input/expected pairs and assertions into sibling `test_cases.py`. In each solution, import `run_cases` only inside `if __name__ == "__main__"` and call `run_cases(Solution())`. This keeps variants reusable while allowing `python3 path/to/solution.py` to test one file.

Use a compact table of cases:

```python
TEST_CASES = [("a + a", "2a")]
```

Add edge cases, counterexamples, and one normal case. Run the relevant script with `python3` before committing. For variants, include expected outputs so differences are clear.

## Commit & Pull Request Guidelines

Recent git history uses short messages such as `update`; prefer a specific imperative message, for example `add gas station binary search notes` or `fix scheduler prob2 counterexample`.

Pull requests should describe the problem changed, list touched solution files, and summarize testing. Link the original problem or issue when available. Include screenshots only for documentation or visual-output changes.

## Agent-Specific Instructions

Do not overwrite unrelated local changes. Keep edits scoped to the requested problem or guide, and preserve exploratory files unless the user asks for cleanup.
