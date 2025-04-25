#include "benchmark.h"
#include <iostream>
#include <chrono>
#include <random>
#include <thread>
#include <algorithm>
#include <fstream>

// Global variables
std::atomic<int>* result_take1;
std::vector<int> result_take2;
std::vector<int> matrix;

// Initialize matrix with random values
void initMatrix() {
    matrix.resize(DIM * DIM);
    std::mt19937 rng(42);  // Use fixed seed for reproducibility
    std::uniform_int_distribution<int> dist(0, 100);
    for (int& val : matrix) {
        val = dist(rng);
    }
}

// Implementation 1: With False Sharing
int runTake1(int num_threads) {
    // Allocate memory for atomic integers
    result_take1 = new std::atomic<int>[num_threads];
    std::vector<std::thread> threads;
    int chunkSize = DIM / num_threads + 1;
    
    // Initialize atomic values
    for (int p = 0; p < num_threads; ++p) {
        result_take1[p] = 0;
    }
    
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int p = 0; p < num_threads; ++p) {
        threads.emplace_back([p, chunkSize, num_threads]() {
            int myStart = p * chunkSize;
            int myEnd = std::min(myStart + chunkSize, DIM);
            for (int i = myStart; i < myEnd; ++i) {
                for (int j = 0; j < DIM; ++j) {
                    if (matrix[i * DIM + j] % 2 != 0)
                        ++result_take1[p];  // 🔥 False Sharing occurs here
                }
            }
        });
    }
    
    for (auto& t : threads) t.join();
    
    int odds = 0;
    for (int p = 0; p < num_threads; ++p)
        odds += result_take1[p];
    
    // Clean up allocated memory
    delete[] result_take1;
        
    auto end = std::chrono::high_resolution_clock::now();
    // Measure time in microseconds
    int time_us = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    int time_ms = time_us / 1000; // Convert to ms for display
    
    std::cout << "[Take 1] Threads: " << num_threads << ", Odd count: " << odds << "\n";
    std::cout << "[Take 1] Time: " << time_ms << " ms (" << time_us << " μs)\n";
    
    return time_us;
}

// Implementation 2: Without False Sharing (Optimized)
int runTake2(int num_threads) {
    result_take2.resize(num_threads);
    std::vector<std::thread> threads;
    int chunkSize = DIM / num_threads + 1;
    
    auto start = std::chrono::high_resolution_clock::now();
    
    for (int p = 0; p < num_threads; ++p) {
        threads.emplace_back([p, chunkSize, num_threads]() {
            int count = 0;  // ✅ Local variable prevents false sharing
            int myStart = p * chunkSize;
            int myEnd = std::min(myStart + chunkSize, DIM);
            for (int i = myStart; i < myEnd; ++i) {
                for (int j = 0; j < DIM; ++j) {
                    if (matrix[i * DIM + j] % 2 != 0)
                        ++count;  // ✅ Local accumulation
                }
            }
            result_take2[p] = count;  // ✅ Write result only once at the end
        });
    }
    
    for (auto& t : threads) t.join();
    
    int odds = 0;
    for (int p = 0; p < num_threads; ++p)
        odds += result_take2[p];
        
    auto end = std::chrono::high_resolution_clock::now();
    // Measure time in microseconds
    int time_us = std::chrono::duration_cast<std::chrono::microseconds>(end - start).count();
    int time_ms = time_us / 1000; // Convert to ms for display
    
    std::cout << "[Take 2] Threads: " << num_threads << ", Odd count: " << odds << "\n";
    std::cout << "[Take 2] Time: " << time_ms << " ms (" << time_us << " μs)\n";
    
    return time_us;
}

// Write results to CSV file
void writeResultsToCsv(const std::vector<BenchmarkResult>& results) {
    std::ofstream file("benchmark_results.csv");
    file << "Threads,Take1_Time_ms,Take2_Time_ms,Take1_Time_us,Take2_Time_us\n";
    
    for (const auto& result : results) {
        file << result.threads << "," 
             << (result.take1_time_us / 1000) << "," 
             << (result.take2_time_us / 1000) << ","
             << result.take1_time_us << ","
             << result.take2_time_us << "\n";
    }
    
    file.close();
    std::cout << "Results written to benchmark_results.csv\n";
}