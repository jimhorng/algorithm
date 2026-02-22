import java.util.Arrays;
import java.util.TreeMap;

public class MainBackwardTreemap {
    public static int minCpus(int[] startTimes, int taskLen) {
        int n = startTimes.length;
        
        Arrays.sort(startTimes);
        int maxStartTime = startTimes[n-1];
        int deadline = maxStartTime + taskLen;
        int cpu = 0;
        
        TreeMap<Integer, Integer> freeStartTimeSlotsMap = new TreeMap<>(); // freeStartTimes, count
        
        // from last to process
        for (int i = n - 1; i >= 0; i--) {
            int time = startTimes[i];
            
            
            Integer t = freeStartTimeSlotsMap.ceilingKey(time);
            if (t == null) { // no free start slot, CPU++
                cpu++;
                int nextFreeStartTime = maxStartTime - taskLen; // will occupy last slots
                
                freeStartTimeSlotsMap.put(nextFreeStartTime, freeStartTimeSlotsMap.getOrDefault(nextFreeStartTime, 0)+1);
                
            } else {
                                
                freeStartTimeSlotsMap.put(t, freeStartTimeSlotsMap.get(t) - 1);
                
                if (freeStartTimeSlotsMap.get(t) == 0) {
                    freeStartTimeSlotsMap.remove(t);
                }
                
                int nextFreeStartTime = t - taskLen; // will occupy last slots
                
                freeStartTimeSlotsMap.put(nextFreeStartTime, freeStartTimeSlotsMap.getOrDefault(nextFreeStartTime, 0)+1);
            }
        }
        return cpu;
        
    }

    private static void runTest(String testName, int[] startTimes, int taskLen, int expected) {
        int result = minCpus(startTimes, taskLen);
        boolean passed = result == expected;
        String status = passed ? "✓" : "✗";
        System.out.printf("%s %s: got %d, expected %d%n", status, testName, result, expected);
        assert result == expected : String.format("%s failed: got %d, expected %d", testName, result, expected);
    }

    public static void main(String[] args) {
        System.out.println("Running tests...\n");
        
        // Test 1: example1_large_gap
        runTest("example1_large_gap", 
                new int[]{0, 0, 0, 10000}, 
                5, 
                1);
        
        // Test 2: example2_all_same_start
        runTest("example2_all_same_start", 
                new int[]{0, 0, 0}, 
                5, 
                3);
        
        // Test 3: single_task
        runTest("single_task", 
                new int[]{0}, 
                10, 
                1);
        
        // Test 4: two_tasks_overlap
        runTest("two_tasks_overlap", 
                new int[]{0, 3}, 
                5, 
                2);
        
        // Test 5: two_tasks_no_overlap
        runTest("two_tasks_no_overlap", 
                new int[]{0, 10}, 
                5, 
                1);
        
        // Test 6: multiple_overlapping
        runTest("multiple_overlapping", 
                new int[]{0, 1, 2, 3, 4}, 
                10, 
                5);
        
        // Test 7: partial_overlap
        runTest("partial_overlap", 
                new int[]{0, 5, 10}, 
                7, 
                2);
        
        // Test 8: fifty_tasks_grouped_overlaps
        runTest("fifty_tasks_grouped_overlaps", 
                new int[]{0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                         10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
                         15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
                         20, 20, 20, 20, 20, 20, 20, 20, 20, 20}, 
                6, 
                20);
        
        // Additional tests from original Main.java
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