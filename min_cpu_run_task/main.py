"""
Main test runner for minimum CPU solutions.
Run with: python main.py [solution_name]
Example: python main.py sol1
"""

import sys
import importlib
from test_cases import test_cases

# Default solution to test
DEFAULT_SOLUTION = "sol1"


def run_tests(solution_func, solution_name="solution"):
    """Run all test cases against a solution function."""
    passed = 0
    failed = 0
    
    print(f"Running tests for {solution_name}...\n")
    
    for i, tc in enumerate(test_cases):
        result = solution_func(tc["start_times"], tc["task_length"])
        is_correct = result == tc["expected"]
        status = "✓" if is_correct else "✗"
        
        if is_correct:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} Test {i+1} ({tc['testcase']}): got {result}, expected {tc['expected']}")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print(f"{'='*60}")
    
    return failed == 0


def main():
    # Default to sol1 if no argument provided
    solution_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SOLUTION
    
    try:
        # Dynamically import the solution module
        solution_module = importlib.import_module(solution_name)
        solution_func = getattr(solution_module, solution_name)
        
        # Run tests
        success = run_tests(solution_func, solution_name)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except (ImportError, AttributeError) as e:
        print(f"Error: Could not load solution '{solution_name}'")
        print(f"Details: {e}")
        print(f"\nUsage: python main.py [solution_name]")
        print(f"Example: python main.py sol1")
        sys.exit(1)


if __name__ == "__main__":
    main()
