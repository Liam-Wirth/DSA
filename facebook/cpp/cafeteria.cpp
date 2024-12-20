long long getMaxAdditionalDinersCount(long long N, long long K, int M, vector<long long> S) {
    // Sort the occupied seats
    sort(S.begin(), S.end());
    
    long long max_diners = 0;
    
    // Check space before the first occupied seat
    if (M > 0) {  // Only if there are occupied seats
        // Calculate available seats before first diner
        long long available_space = S[0] - 1;  // Space from 1 to first occupied seat
        max_diners += (available_space) / (K + 1);
        
        // Check spaces between occupied seats
        for (int i = 1; i < M; i++) {
            available_space = (S[i] - S[i-1] - 1) - K;  // Remove K seats on both sides
            if (available_space > 0) {
                max_diners += (available_space) / (K + 1);
            }
        }
        
        // Check space after the last occupied seat
        available_space = N - (S[M-1] + K);  // Space from last occupied + K to N
        if (available_space > 0) {
            max_diners += (available_space + K) / (K + 1);
        }
    } else {
        // If no seats are occupied, we can use the entire table
        max_diners = (N + K) / (K + 1);
    }
    
    return max_diners;
}
