#pragma once

#include <vector>
#include <atomic>

// Matrix size
constexpr int DIM = 10000;

// Result structure for the benchmark
struct BenchmarkResult {
    int threads;
    int take1_time_us;  // Time in microseconds for approach with false sharing
    int take2_time_us;  // Time in microseconds for optimized approach
};

// Function declarations
void initMatrix();
int runTake1(int num_threads);  // Returns execution time in microseconds
int runTake2(int num_threads);  // Returns execution time in microseconds
void writeResultsToCsv(const std::vector<BenchmarkResult>& results);

// Global variables (defined in benchmark.cpp)
extern std::atomic<int>* result_take1;
extern std::vector<int> result_take2;
extern std::vector<int> matrix;