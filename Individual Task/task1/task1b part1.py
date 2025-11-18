# Task 1: Operational Station Status System
# Task 1b Part 1: Empirical Performance Measurement
# Riyah Hussain

import os, sys, random, time
import matplotlib.pyplot as plt
import numpy as np

# -point Python at the CLRS folders-
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, "clrsPython")

sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 11"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 10"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 31"))

from chained_hashtable import ChainedHashTable
from hash_functions import hashpjw

class StationStatusTracker:
    """Track operational status using chained hash table."""

    def __init__(self, table_size):
        self.operational_stations = ChainedHashTable(table_size, hash_func=hashpjw)
        self.table_size = table_size

    def mark_operational(self, station_name):
        """Add station to operational list."""
        self.operational_stations.insert(station_name)

    def is_operational(self, station_name):
        """Check if station is operational - PRIMARY QUERY."""
        result = self.operational_stations.search(station_name)
        return result is not None


def generate_station_dataset(n):
    """Generate n unique station names as integers from 0 to n-1."""
    return list(range(n))


def build_data_structure(stations, table_size):
    """Build the hash table with all stations marked as operational."""
    tracker = StationStatusTracker(table_size)
    for station in stations:
        tracker.mark_operational(station)
    return tracker


def measure_average_query_time(tracker, stations, num_queries=10000):
    """
    Measure average time per status check over random queries.

    Args:
        tracker: StationStatusTracker instance
        stations: list of station names to query from
        num_queries: number of random queries to perform

    Returns:
        Average time per query in microseconds
    """
    total_time = 0.0

    for _ in range(num_queries):
        # Random station from the dataset
        station = random.choice(stations)

        # Measure query time
        start = time.perf_counter()
        tracker.is_operational(station)
        end = time.perf_counter()

        total_time += (end - start)

    # Return average time in microseconds
    avg_time_microseconds = (total_time / num_queries) * 1_000_000
    return avg_time_microseconds


def find_next_prime(n):
    """Find the next prime number greater than or equal to n."""

    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    while not is_prime(n):
        n += 1
    return n


def run_performance_analysis(dataset_sizes, num_queries=10000):
    """
    Run performance analysis for different dataset sizes.

    Args:
        dataset_sizes: list of n values to test
        num_queries: number of queries per dataset size

    Returns:
        Dictionary with results
    """
    results = {
        'n_values': [],
        'avg_times': [],
        'load_factors': [],
        'table_sizes': []
    }

    print("=" * 70)
    print("EMPIRICAL PERFORMANCE MEASUREMENT")
    print("=" * 70)
    print(f"Number of queries per dataset: {num_queries:,}")
    print()

    for n in dataset_sizes:
        print(f"Testing n = {n:,}...")

        # Generate dataset
        stations = generate_station_dataset(n)

        # Choose table size as next prime >= n (for better hash distribution)
        table_size = find_next_prime(n)

        # Build data structure
        tracker = build_data_structure(stations, table_size)

        # Measure average query time
        avg_time = measure_average_query_time(tracker, stations, num_queries)

        # Calculate load factor
        load_factor = n / table_size

        # Store results
        results['n_values'].append(n)
        results['avg_times'].append(avg_time)
        results['load_factors'].append(load_factor)
        results['table_sizes'].append(table_size)

        print(f"  Table size: {table_size}")
        print(f"  Load factor (α): {load_factor:.3f}")
        print(f"  Average query time: {avg_time:.4f} μs")
        print(f"  Queries per second: {1_000_000 / avg_time:,.0f}")
        print()

    return results


def plot_results(results):
    """
    Plot average time per check versus dataset size.
    """
    n_values = results['n_values']
    avg_times = results['avg_times']

    plt.figure(figsize=(12, 8))

    # Plot 1: Average Query Time vs Dataset Size
    plt.subplot(2, 1, 1)
    plt.plot(n_values, avg_times, 'bo-', linewidth=2, markersize=8, label='Empirical Data')

    # Theoretical O(1) - horizontal line at mean
    theoretical_constant = np.mean(avg_times)
    plt.axhline(y=theoretical_constant, color='r', linestyle='--',
                linewidth=2, label=f'Theoretical O(1) (mean = {theoretical_constant:.4f} μs)')

    plt.xlabel('Dataset Size (n)', fontsize=12, fontweight='bold')
    plt.ylabel('Average Query Time (μs)', fontsize=12, fontweight='bold')
    plt.title('Hash Table Performance: Average Query Time vs Dataset Size',
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    # Plot 2: Load Factor vs Dataset Size
    plt.subplot(2, 1, 2)
    plt.plot(n_values, results['load_factors'], 'go-', linewidth=2, markersize=8)
    plt.xlabel('Dataset Size (n)', fontsize=12, fontweight='bold')
    plt.ylabel('Load Factor (α = n/m)', fontsize=12, fontweight='bold')
    plt.title('Hash Table Load Factor vs Dataset Size', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='α = 1.0')
    plt.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
    print("Graph saved as 'performance_analysis.png'")
    plt.show()


def analyze_alignment(results):
    """
    Analyze alignment between empirical results and theoretical O(1) complexity.
    """
    print("=" * 70)
    print("THEORETICAL vs EMPIRICAL ANALYSIS")
    print("=" * 70)

    avg_times = results['avg_times']
    n_values = results['n_values']

    # Calculate statistics
    mean_time = np.mean(avg_times)
    std_time = np.std(avg_times)
    coefficient_of_variation = (std_time / mean_time) * 100

    print(f"\nTheoretical Complexity: O(1) - constant time")
    print(f"\nEmpirical Results:")
    print(f"  Mean query time: {mean_time:.4f} μs")
    print(f"  Standard deviation: {std_time:.4f} μs")
    print(f"  Coefficient of variation: {coefficient_of_variation:.2f}%")
    print(f"  Min time: {min(avg_times):.4f} μs (at n={n_values[avg_times.index(min(avg_times))]})")
    print(f"  Max time: {max(avg_times):.4f} μs (at n={n_values[avg_times.index(max(avg_times))]})")

    # Check if times remain relatively constant
    time_range = max(avg_times) - min(avg_times)
    print(f"  Range: {time_range:.4f} μs")

    print(f"\nAlignment Assessment:")
    if coefficient_of_variation < 10:
        print("  ✓ EXCELLENT: Query times remain nearly constant across all dataset sizes.")
        print("    This strongly confirms O(1) theoretical complexity.")
    elif coefficient_of_variation < 20:
        print("  ✓ GOOD: Query times show minor variation but remain relatively constant.")
        print("    This aligns well with O(1) theoretical complexity.")
    else:
        print("  ⚠ MODERATE: Some variation observed in query times.")

    print(f"\nPossible Discrepancy Factors:")
    print("  • Load factor variations (α = n/m affects chain lengths)")
    print("  • Hash collisions increase slightly with larger datasets")
    print("  • Cache effects and memory access patterns")
    print("  • Python's memory management overhead")
    print("  • System background processes during measurement")

    # Calculate growth rate
    if len(n_values) > 1:
        time_growth = ((avg_times[-1] - avg_times[0]) / avg_times[0]) * 100
        size_growth = ((n_values[-1] - n_values[0]) / n_values[0]) * 100
        print(f"\nGrowth Analysis:")
        print(f"  Dataset size increased by: {size_growth:.1f}%")
        print(f"  Query time increased by: {time_growth:.1f}%")
        print(f"  Growth ratio (time/size): {time_growth / size_growth:.4f}")

        if abs(time_growth) < 20:
            print("  → Time complexity appears constant (O(1)) ✓")
        else:
            print("  → Some growth observed, but significantly less than dataset growth")


if __name__ == "__main__":
    # Define dataset sizes to test
    dataset_sizes = [1000, 5000, 10000, 25000, 50000]

    # Run performance analysis
    results = run_performance_analysis(dataset_sizes, num_queries=10000)

    # Plot results
    plot_results(results)

    # Analyze alignment with theoretical complexity
    analyze_alignment(results)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

import os, sys, random, time
import matplotlib.pyplot as plt
import numpy as np

# -points Python at the CLRS folders-
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, "clrsPython")

# sys.path points to the CLRS implementation
# added CLRS subfolders so `X import Y` works
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 11"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 10"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 31"))

from chained_hashtable import ChainedHashTable
from hash_functions import hashpjw

class StationStatusTracker:
    """Track operational status using chained hash table."""

    def __init__(self, table_size):
        self.operational_stations = ChainedHashTable(table_size, hash_func=hashpjw)
        self.table_size = table_size

    def mark_operational(self, station_name):
        """Add station to operational list."""
        self.operational_stations.insert(station_name)

    def is_operational(self, station_name):
        """Check if station is operational - PRIMARY QUERY."""
        result = self.operational_stations.search(station_name)
        return result is not None


def generate_station_dataset(n):
    """Generate n unique station names as integers from 0 to n-1."""
    return list(range(n))


def build_data_structure(stations, table_size):
    """Build the hash table with all stations marked as operational."""
    tracker = StationStatusTracker(table_size)
    for station in stations:
        tracker.mark_operational(station)
    return tracker


def measure_average_query_time(tracker, stations, num_queries=10000):
    """
    Measure average time per status check over random queries.

    Args:
        tracker: StationStatusTracker instance
        stations: list of station names to query from
        num_queries: number of random queries to perform

    Returns:
        Average time per query in microseconds
    """
    total_time = 0.0

    for _ in range(num_queries):
        # Random station from the dataset
        station = random.choice(stations)

        # Measure query time
        start = time.perf_counter()
        tracker.is_operational(station)
        end = time.perf_counter()

        total_time += (end - start)

    # Return average time in microseconds
    avg_time_microseconds = (total_time / num_queries) * 1_000_000
    return avg_time_microseconds


def find_next_prime(n):
    """Find the next prime number greater than or equal to n."""

    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    while not is_prime(n):
        n += 1
    return n


def run_performance_analysis(dataset_sizes, num_queries=10000):
    """
    Run performance analysis for different dataset sizes.

    Args:
        dataset_sizes: list of n values to test
        num_queries: number of queries per dataset size

    Returns:
        Dictionary with results
    """
    results = {
        'n_values': [],
        'avg_times': [],
        'load_factors': [],
        'table_sizes': []
    }

    print("=" * 70)
    print("EMPIRICAL PERFORMANCE MEASUREMENT")
    print("=" * 70)
    print(f"Number of queries per dataset: {num_queries:,}")
    print()

    for n in dataset_sizes:
        print(f"Testing n = {n:,}...")

        # Generate dataset
        stations = generate_station_dataset(n)

        # Choose table size as next prime >= n (for better hash distribution)
        table_size = find_next_prime(n)

        # Build data structure
        tracker = build_data_structure(stations, table_size)

        # Measure average query time
        avg_time = measure_average_query_time(tracker, stations, num_queries)

        # Calculate load factor
        load_factor = n / table_size

        # Store results
        results['n_values'].append(n)
        results['avg_times'].append(avg_time)
        results['load_factors'].append(load_factor)
        results['table_sizes'].append(table_size)

        print(f"  Table size: {table_size}")
        print(f"  Load factor (α): {load_factor:.3f}")
        print(f"  Average query time: {avg_time:.4f} μs")
        print(f"  Queries per second: {1_000_000 / avg_time:,.0f}")
        print()

    return results


def plot_results(results):
    """
    Plot average time per check versus dataset size.
    """
    n_values = results['n_values']
    avg_times = results['avg_times']

    plt.figure(figsize=(12, 8))

    # Plot1: Average Query Time vs Dataset Size
    plt.subplot(2, 1, 1)
    plt.plot(n_values, avg_times, 'bo-', linewidth=2, markersize=8, label='Empirical Data')

    # Theoretical O(1) - horizontal line at mean
    theoretical_constant = np.mean(avg_times)
    plt.axhline(y=theoretical_constant, color='r', linestyle='--',
                linewidth=2, label=f'Theoretical O(1) (mean = {theoretical_constant:.4f} μs)')

    plt.xlabel('Dataset Size (n)', fontsize=12, fontweight='bold')
    plt.ylabel('Average Query Time (μs)', fontsize=12, fontweight='bold')
    plt.title('Hash Table Performance: Average Query Time vs Dataset Size',
              fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    # Plot2: Load Factor vs Dataset Size
    plt.subplot(2, 1, 2)
    plt.plot(n_values, results['load_factors'], 'go-', linewidth=2, markersize=8)
    plt.xlabel('Dataset Size (n)', fontsize=12, fontweight='bold')
    plt.ylabel('Load Factor (α = n/m)', fontsize=12, fontweight='bold')
    plt.title('Hash Table Load Factor vs Dataset Size', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='α = 1.0')
    plt.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
    print("Graph saved as 'performance_analysis.png'")
    plt.show()


def analyze_alignment(results):
    """
    Analyze alignment between empirical results and theoretical O(1) complexity.
    """
    print("=" * 70)
    print("THEORETICAL vs EMPIRICAL ANALYSIS")
    print("=" * 70)

    avg_times = results['avg_times']
    n_values = results['n_values']

    # Calculate statistics
    mean_time = np.mean(avg_times)
    std_time = np.std(avg_times)
    coefficient_of_variation = (std_time / mean_time) * 100

    print(f"\nTheoretical Complexity: O(1) - constant time")
    print(f"\nEmpirical Results:")
    print(f"  Mean query time: {mean_time:.4f} μs")
    print(f"  Standard deviation: {std_time:.4f} μs")
    print(f"  Coefficient of variation: {coefficient_of_variation:.2f}%")
    print(f"  Min time: {min(avg_times):.4f} μs (at n={n_values[avg_times.index(min(avg_times))]})")
    print(f"  Max time: {max(avg_times):.4f} μs (at n={n_values[avg_times.index(max(avg_times))]})")

    # Check if times remain relatively constant
    time_range = max(avg_times) - min(avg_times)
    print(f"  Range: {time_range:.4f} μs")

    print(f"\nAlignment Assessment:")
    if coefficient_of_variation < 10:
        print("  ✓ EXCELLENT: Query times remain nearly constant across all dataset sizes.")
        print("    This strongly confirms O(1) theoretical complexity.")
    elif coefficient_of_variation < 20:
        print("  ✓ GOOD: Query times show minor variation but remain relatively constant.")
        print("    This aligns well with O(1) theoretical complexity.")
    else:
        print("  ⚠ MODERATE: Some variation observed in query times.")

    print(f"\nPossible Discrepancy Factors:")
    print("  • Load factor variations (α = n/m affects chain lengths)")
    print("  • Hash collisions increase slightly with larger datasets")
    print("  • Cache effects and memory access patterns")
    print("  • Python's memory management overhead")
    print("  • System background processes during measurement")

    # Calculate growth rate
    if len(n_values) > 1:
        time_growth = ((avg_times[-1] - avg_times[0]) / avg_times[0]) * 100
        size_growth = ((n_values[-1] - n_values[0]) / n_values[0]) * 100
        print(f"\nGrowth Analysis:")
        print(f"  Dataset size increased by: {size_growth:.1f}%")
        print(f"  Query time increased by: {time_growth:.1f}%")
        print(f"  Growth ratio (time/size): {time_growth / size_growth:.4f}")

        if abs(time_growth) < 20:
            print("  → Time complexity appears constant (O(1)) ✓")
        else:
            print("  → Some growth observed, but significantly less than dataset growth")


if __name__ == "__main__":
    # Define dataset sizes to test
    dataset_sizes = [1000, 5000, 10000, 25000, 50000]

    # Run performance analysis
    results = run_performance_analysis(dataset_sizes, num_queries=10000)

    # Plot results
    plot_results(results)

    # Analyze alignment with theoretical complexity
    analyze_alignment(results)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
