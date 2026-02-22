import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Collections;

public class MainMaxHeap {
    public static int minCpus(int[] startTimes, int taskLen) {
        int n = startTimes.length;
        
        Arrays.sort(startTimes);
        int maxStartTime = startTimes[n-1];
        
        // Max heap: stores CPUs by their max free time before next occupied slot (largest first)
        PriorityQueue<Integer> maxFreeTimeBeforeSlot = new PriorityQueue<>(Collections.reverseOrder());
        
        // Process tasks from last to first
        for (int i = n - 1; i >= 0; i--) {
            int currentTaskStart = startTimes[i];
            int currentTaskEnd = currentTaskStart + taskLen;
            
            if (!maxFreeTimeBeforeSlot.isEmpty()) {
                // Try to use CPU with largest free time
                int largestFreeTime = maxFreeTimeBeforeSlot.peek();
                
                // Check if current task can fit before the occupied period
                if (currentTaskEnd <= largestFreeTime) {
                    // Can reuse this CPU - task fits in the free time
                    maxFreeTimeBeforeSlot.poll();
                    // Update free time: task now occupies this slot, 
                    // so free time moves earlier by task duration
                    maxFreeTimeBeforeSlot.offer(largestFreeTime - taskLen);
                } else {
                    // Cannot fit, need a new CPU
                    // New CPU is free up to maxStartTime
                    maxFreeTimeBeforeSlot.offer(maxStartTime);
                }
            } else {
                // No CPUs yet, allocate first one
                // This CPU is free up to maxStartTime
                maxFreeTimeBeforeSlot.offer(maxStartTime);
            }
        }
        
        return maxFreeTimeBeforeSlot.size();
    }

    private static void runTest(String testName, int[] startTimes, int taskLen, int expected) {
        int result = minCpus(startTimes, taskLen);
        boolean passed = result == expected;
        String status = passed ? "✓" : "✗";
        System.out.printf("%s %s: got %d, expected %d%n", status, testName, result, expected);
        assert result == expected : String.format("%s failed: got %d, expected %d", testName, result, expected);
    }

    public static void main(String[] args) {
        System.out.println("Running tests with Max Heap approach...\n");
        
        runTest("example1_large_gap", 
                new int[]{0, 0, 0, 10000}, 
                5, 
                1);
        
        runTest("example2_all_same_start", 
                new int[]{0, 0, 0}, 
                5, 
                3);
        
        runTest("single_task", 
                new int[]{0}, 
                10, 
                1);
        
        runTest("two_tasks_overlap", 
                new int[]{0, 3}, 
                5, 
                2);
        
        runTest("two_tasks_no_overlap", 
                new int[]{0, 10}, 
                5, 
                1);
        
        runTest("multiple_overlapping", 
                new int[]{0, 1, 2, 3, 4}, 
                10, 
                5);
        
        runTest("partial_overlap", 
                new int[]{0, 5, 10}, 
                7, 
                2);
        
        runTest("fifty_tasks_grouped_overlaps", 
                new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                         10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                         15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
                         20, 20, 20, 20, 20, 20, 20, 20, 20, 20}, 
                6, 
                20);
        
        runTest("additional_test_1", 
                new int[]{0, 4, 4}, 
                5, 
                3);
        
        runTest("additional_test_2", 
                new int[]{0, 1, 2, 4, 5}, 
                3, 
                3);
        
        runTest("additional_test_3", 
                new int[]{0, 5, 10, 15}, 
                5, 
                1);
        
        runTest("additional_test_4", 
                new int[]{0, 4, 9, 9}, 
                5, 
                2);
        
        System.out.println("\n============================================================");
        System.out.println("All tests passed!");
        System.out.println("============================================================");
    }
}
