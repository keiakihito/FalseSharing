import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set the style for the plots
sns.set(style="darkgrid")

# Read the CSV file
df = pd.read_csv('benchmark_results.csv')

# Check if microsecond columns are in the CSV directly
if 'Take1_Time_us' in df.columns and 'Take2_Time_us' in df.columns:
    # Use microsecond columns directly
    print("Using microsecond data from CSV file directly")
else:
    # Convert milliseconds to microseconds (1 ms = 1000 μs)
    print("Converting millisecond data to microseconds")
    df['Take1_Time_us'] = df['Take1_Time_ms'] * 1000
    df['Take2_Time_us'] = df['Take2_Time_ms'] * 1000

# Create a figure and axis with more appropriate sizing and explicit margins
plt.figure(figsize=(14, 10))
# Set figure with explicit subplot parameters to avoid tight layout warnings
plt.subplots_adjust(left=0.1, right=0.85, top=0.85, bottom=0.1)

# Create primary Y axis for execution times
ax1 = plt.gca()

# Plot the two approaches with microsecond scale
line1, = ax1.plot(df['Threads'], df['Take1_Time_us'], 'o-', color='#e74c3c', linewidth=2, markersize=8)
line2, = ax1.plot(df['Threads'], df['Take2_Time_us'], 's-', color='#2ecc71', linewidth=2, markersize=8)

# Set labels for primary Y axis with microsecond unit
ax1.set_ylabel('Execution Time (μs)', fontsize=14, color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Create secondary Y axis for speedup ratio
ax2 = ax1.twinx()
line3, = ax2.plot(df['Threads'], df['Take1_Time_ms'] / df['Take2_Time_ms'], '--', color='#3498db', linewidth=2)
ax2.set_ylabel('Speedup Ratio', fontsize=14, color='#3498db')
ax2.tick_params(axis='y', labelcolor='#3498db')
ax2.grid(False)

# Add title and x label
plt.title('Performance Comparison: False Sharing vs Optimized Approach', fontsize=18, pad=15)
ax1.set_xlabel('Number of Threads', fontsize=14)

# Create a proper legend that clearly shows what each line represents
# First, create a custom legend with proper labels
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='#e74c3c', label='Take 1: With False Sharing', markersize=8, linestyle='-', linewidth=2),
    plt.Line2D([0], [0], marker='s', color='#2ecc71', label='Take 2: Without False Sharing', markersize=8, linestyle='-', linewidth=2),
    plt.Line2D([0], [0], color='#3498db', label='Speedup Ratio (Take1/Take2)', linestyle='--', linewidth=2)
]

# Place the legend at the top of the figure to avoid overlap
legend = plt.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 1.15), 
                    ncol=3, frameon=True, fontsize=12)

# Make sure x-axis explicitly shows thread numbers
thread_count = len(df['Threads'])
if thread_count <= 15:
    ax1.set_xticks(df['Threads'])
else:
    # Show appropriate number of ticks
    step = max(1, len(df['Threads']) // 10)
    ax1.set_xticks(df['Threads'][::step])

# Find optimal number of threads for both approaches and convert to microseconds
optimal_threads_take1 = df.loc[df['Take1_Time_us'].idxmin(), 'Threads']
optimal_threads_take2 = df.loc[df['Take2_Time_us'].idxmin(), 'Threads']
min_time_take1 = df['Take1_Time_us'].min()
min_time_take2 = df['Take2_Time_us'].min()

# Add annotations for optimal thread counts with microsecond values
ax1.annotate(f'Optimal: {optimal_threads_take1} threads ({int(min_time_take1)} μs)', 
             xy=(optimal_threads_take1, min_time_take1),
             xytext=(optimal_threads_take1 + 1, min_time_take1 + 5000),  # Adjusted for microsecond scale
             arrowprops=dict(facecolor='#e74c3c', width=1.5, headwidth=7, shrink=0.05),
             fontsize=11, color='#e74c3c', fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#e74c3c", alpha=0.8))

ax1.annotate(f'Optimal: {optimal_threads_take2} threads ({int(min_time_take2)} μs)', 
             xy=(optimal_threads_take2, min_time_take2),
             xytext=(optimal_threads_take2 + 1, min_time_take2 + 1000),  # Adjusted for microsecond scale
             arrowprops=dict(facecolor='#2ecc71', width=1.5, headwidth=7, shrink=0.05),
             fontsize=11, color='#2ecc71', fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#2ecc71", alpha=0.8))

# Calculate summary statistics with microsecond values
speedup = df['Take1_Time_us'] / df['Take2_Time_us']
max_speedup = speedup.max()
max_speedup_threads = df.loc[speedup.idxmax(), 'Threads']

# Add a properly positioned summary text box with microsecond values
textstr = '\n'.join((
    'Summary:',
    f'Average speedup: {speedup.mean():.2f}x',
    f'Max speedup: {max_speedup:.2f}x at {max_speedup_threads} threads',
    f'Take 1 min time: {int(min_time_take1)} μs at {optimal_threads_take1} threads',
    f'Take 2 min time: {int(min_time_take2)} μs at {optimal_threads_take2} threads'
))

# Position the text box in the bottom right with better styling
props = dict(boxstyle='round4,pad=0.7', facecolor='white', alpha=0.9, ec='gray')
plt.gcf().text(0.75, 0.15, textstr, fontsize=11,
               verticalalignment='bottom', horizontalalignment='center',
               bbox=props)

# Adjust layout with explicit control rather than using tight_layout
plt.subplots_adjust(top=0.82, bottom=0.1, left=0.1, right=0.88)  # Make room for the legend and right y-axis

# Save figure with high resolution and add a bit more padding
plt.savefig('benchmark_results.png', dpi=300, bbox_inches='tight', pad_inches=0.5)
plt.show()

print("Plot has been saved as 'benchmark_results.png'")

# Additional analysis for terminal output with microsecond values
print("\nDetailed Analysis:")
print(f"Take 1 (False Sharing) - Min time: {int(min_time_take1)} μs at {optimal_threads_take1} threads")
print(f"Take 2 (Optimized) - Min time: {int(min_time_take2)} μs at {optimal_threads_take2} threads")
print(f"Average speedup of Take 2 over Take 1: {speedup.mean():.2f}x")
print(f"Maximum speedup: {max_speedup:.2f}x at {max_speedup_threads} threads")

# Create a second plot focusing on scaling efficiency with proper layout
plt.figure(figsize=(14, 8))
# Set figure with explicit subplot parameters
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

# Calculate ideal scaling (assuming perfect parallelism from minimum thread count) - using microsecond values
base_thread = df['Threads'].min()
base_time_take1 = df.loc[df['Threads'] == base_thread, 'Take1_Time_us'].values[0]
base_time_take2 = df.loc[df['Threads'] == base_thread, 'Take2_Time_us'].values[0]

efficiency_take1 = [(base_time_take1 * base_thread) / (t * time) * 100 for t, time in zip(df['Threads'], df['Take1_Time_us'])]
efficiency_take2 = [(base_time_take2 * base_thread) / (t * time) * 100 for t, time in zip(df['Threads'], df['Take2_Time_us'])]

plt.plot(df['Threads'], efficiency_take1, 'o-', color='#e74c3c', linewidth=2, markersize=8)
plt.plot(df['Threads'], efficiency_take2, 's-', color='#2ecc71', linewidth=2, markersize=8)

plt.title('Parallel Efficiency: False Sharing vs Optimized Approach', fontsize=18)
plt.xlabel('Number of Threads', fontsize=14)
plt.ylabel('Efficiency (%)', fontsize=14)

if thread_count <= 15:
    plt.xticks(df['Threads'])
else:
    step = max(1, len(df['Threads']) // 10)
    plt.xticks(df['Threads'][::step])

plt.ylim(0, 110)
plt.axhline(y=100, color='gray', linestyle='--', alpha=0.7)

# Create proper legend for efficiency plot
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='#e74c3c', label='Take 1: With False Sharing', markersize=8, linestyle='-', linewidth=2),
    plt.Line2D([0], [0], marker='s', color='#2ecc71', label='Take 2: Without False Sharing', markersize=8, linestyle='-', linewidth=2),
    plt.Line2D([0], [0], color='gray', label='Ideal Efficiency (100%)', linestyle='--', linewidth=2)
]

plt.legend(handles=legend_elements, loc='upper right', frameon=True, fontsize=12)
# Use explicit layout adjustment instead of tight_layout
plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.1)
plt.savefig('efficiency_analysis.png', dpi=300, bbox_inches='tight', pad_inches=0.5)
plt.show()

print("Efficiency analysis plot has been saved as 'efficiency_analysis.png'")