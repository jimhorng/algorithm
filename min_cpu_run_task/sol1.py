"""
1) set min overlaps from 1 to n
2) each round try start task asap, check if final task can start in start time
    4) track task exceed start_times as count, and end times for avaiable slot for new ready-to-start task
    5) at most min overlaps for each round
3) binary search for min overlaps
"""

from collections import deque

def _simulate(sorted_start_times, task_length, num_cpus, min_possible_end):
    """
    Simulate scheduling with given number of CPUs.
    Returns True if can meet min end time, False otherwise.
    """
    n = len(sorted_start_times)
    cpu_times = deque([0] * num_cpus)
    
    for i, start_time in enumerate(sorted_start_times):
        earliest_available = cpu_times.popleft()
        actual_start = max(start_time, earliest_available)
        
        # Early stop: if last task can't start on time, we can't meet min end time
        if i == n - 1 and actual_start > start_time:
            return False
        
        end_time = actual_start + task_length
        cpu_times.append(end_time)
    
    return True

def _binary_search_min_cpus(sorted_start_times, task_length, min_possible_end):
    """
    Binary search for minimum number of CPUs that achieves min_possible_end.
    """
    n = len(sorted_start_times)
    left, right = 1, n
    result = n
    
    while left <= right:
        mid = (left + right) // 2
        can_meet_deadline = _simulate(sorted_start_times, task_length, mid, min_possible_end)
        
        if can_meet_deadline:
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    
    return result

def sol1(start_times, task_length):
    if not start_times:
        return 0
    
    sorted_start_times = sorted(start_times)
    min_possible_end = sorted_start_times[-1] + task_length
    
    return _binary_search_min_cpus(sorted_start_times, task_length, min_possible_end)