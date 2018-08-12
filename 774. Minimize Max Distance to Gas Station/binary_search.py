class Solution:
    def minmaxGasDist(self, stations, K):
        """
        :type stations: List[int]
        :type K: int
        :rtype: float
        """
        import math
        delta = 10 ** -6
        dists = [ stations[i+1]-stations[i] for i in range(len(stations)-1) ]
        dist_max = max(dists)
        low, high = 0, dist_max
        while (high-low) > delta:
            mid = (low + high)/2
            k_used = 0
            dist_max_new = 0
            for d in dists:
                splits = math.ceil(d/mid)
                k_used += splits - 1
                dist_max_new = max(dist_max_new, d / splits)
            # print("(", low, mid, high, ")", "dist_max_new:", dist_max_new, "k_used:", k_used)
            if k_used == K:
                return dist_max_new
            elif k_used > K:
                low = mid
            else:
                high = mid
        return low
