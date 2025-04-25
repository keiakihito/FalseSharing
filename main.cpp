#include "benchmark.h"
#include <iostream>
#include <thread>
#include <chrono>

int main() {
    // Initialize the matrix with random values
    initMatrix();
    
    // Get the number of available hardware threads
    int max_threads = std::thread::hardware_concurrency();
    std::cout << "Detected " << max_threads << " hardware threads on your system.\n";
    
    // Set minimum and maximum thread counts for benchmark
    int min_threads = 2;  // Start with at least 2 threads
    int max_threads_to_test = std::min(32, max_threads * 2);  // Test up to 2x hardware threads, max 32
    
    std::cout << "=== Running benchmarks for thread counts " << min_threads << "-" << max_threads_to_test << " ===\n";
    
    // Run benchmarks for each thread count
    std::vector<BenchmarkResult> benchmark_results;
    for (int threads = min_threads; threads <= max_threads_to_test; ++threads) {
        std::cout << "\nRunning with " << threads << " threads\n";
        
        BenchmarkResult result;
        result.threads = threads;
        
        // Run both versions of the algorithm
        result.take1_time_us = runTake1(threads);
        result.take2_time_us = runTake2(threads);
        
        benchmark_results.push_back(result);
        
        // Add a small delay between tests to let the system cool down
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    // Write results to CSV file
    writeResultsToCsv(benchmark_results);
    
    return 0;
}