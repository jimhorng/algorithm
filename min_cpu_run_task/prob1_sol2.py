"""
Backward processing with max heap approach
- Track free time boundary for each CPU
- Process tasks from last to first
- Greedily use CPU with largest free time
"""

import heapq

def prob1(start_times, task_length):
    if not start_times:
        return 0
    
    sorted_start_times = sorted(start_times)
    max_start_time = sorted_start_times[-1]
    
    # Max heap: stores free time boundaries (negate for max heap behavior)
    # Each value represents the latest time a CPU can start a new task
    max_free_time_heap = []
    
    # Process tasks backwards
    for i in range(len(sorted_start_times) - 1, -1, -1):
        current_task_start = sorted_start_times[i]
        current_task_end = current_task_start + task_length
        
        if max_free_time_heap:
            # Get CPU with largest free time (negate to get actual value)
            largest_free_time = -max_free_time_heap[0]
            
            # Check if current task can fit before the occupied period
            if current_task_end <= largest_free_time:
                # Can reuse this CPU
                heapq.heappop(max_free_time_heap)
                # Update free time: move boundary earlier by task_length
                new_free_time = largest_free_time - task_length
                heapq.heappush(max_free_time_heap, -new_free_time)
            else:
                # Cannot fit, need a new CPU
                # New CPU is free up to max_start_time
                heapq.heappush(max_free_time_heap, -max_start_time)
        else:
            # No CPUs yet, allocate first one
            heapq.heappush(max_free_time_heap, -max_start_time)
    
    return len(max_free_time_heap)
