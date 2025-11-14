# Task 1: Operational Station Status System
# Task 1b Part 2: Application with London Underground Data
# Riyah Hussain

import os, sys, csv

# -Point Python at the CLRS folders-
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, "clrsPython")

sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 11"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 10"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 31"))

from chained_hashtable import ChainedHashTable
from hash_functions import hashpjw

class LondonUndergroundStatusSystem:
    """Station status tracking system using chained hash table."""

    def __init__(self, table_size):
        self.operational_stations = ChainedHashTable(table_size, hash_func=hashpjw)
        self.table_size = table_size
        self.station_count = 0

    def mark_operational(self, station_name):
        """Add a station to the operational list."""
        normalized_name = station_name.strip()
        self.operational_stations.insert(normalized_name)
        self.station_count += 1

    def check_status(self, station_name):
        """Check if a station is operational."""
        normalized_name = station_name.strip()
        result = self.operational_stations.search(normalized_name)

        if result is not None:
            return f"✓ '{station_name}' is OPERATIONAL"
        else:
            return f"✗ '{station_name}' is NOT FOUND (not in the system)"


def find_next_prime(n):
    """Find the next prime number >= n."""

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


def extract_stations_from_csv(filename):
    """
    Extract unique station names from CSV file.
    Method: Parse CSV and extract from columns 2 and 3, use set for uniqueness.
    """
    unique_stations = set()

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 2:
                    station1 = row[1].strip()
                    if station1:
                        unique_stations.add(station1)
                    if len(row) >= 3:
                        station2 = row[2].strip()
                        if station2:
                            unique_stations.add(station2)

        return sorted(list(unique_stations))

    except FileNotFoundError:
        print(f"ERROR: File '{filename}' not found.")
        return []


def main():
    print("\n" + "=" * 70)
    print("LONDON UNDERGROUND STATION STATUS SYSTEM - Task 1b Part 2")
    print("=" * 70 + "\n")

    # === STEP 1: Data Acquisition ===
    print("STEP 1: DATA ACQUISITION")
    print("-" * 70)
    print("Method: Python CSV parsing script")
    print("Description: Extracts station names from CSV columns 2 & 3,")
    print("             uses Python set to eliminate duplicates.\n")

    csv_filename = os.path.join(PROJECT_ROOT, "data", "London_Underground_data.csv")
    stations = extract_stations_from_csv(csv_filename)

    if not stations:
        print("✗ Failed to load data. Exiting.\n")
        return

    print(f"✓ Extracted {len(stations)} unique stations\n")

    # Show sample
    print("Sample stations (first 10):")
    for i, station in enumerate(stations[:10], 1):
        print(f"  {i:2d}. {station}")
    print(f"  ... and {len(stations) - 10} more\n")

    # === STEP 2: Implementation ===
    print("=" * 70)
    print("STEP 2: POPULATING SYSTEM")
    print("-" * 70)

    table_size = find_next_prime(len(stations))
    system = LondonUndergroundStatusSystem(table_size)

    print(f"Hash table size (prime): {table_size}")
    print(f"Loading {len(stations)} stations...")

    for station in stations:
        system.mark_operational(station)

    load_factor = system.station_count / system.table_size
    print(f"✓ System populated!")
    print(f"  Total stations: {system.station_count}")
    print(f"  Load factor (α): {load_factor:.3f}\n")

    # === STEP 3: Testing ===
    print("=" * 70)
    print("STEP 3: TESTING STATION STATUS QUERIES")
    print("-" * 70 + "\n")

    test_queries = [
        ("Victoria", "Valid station"),
        ("Baker Street", "Valid station"),
        ("King's Cross St. Pancras", "Valid with special chars"),
        ("Paddinton", "Misspelled 'Paddington'"),
        ("Hogwarts", "Fictional station"),
        ("Westminster Abbey", "Not a tube station"),
    ]

    for i, (query, desc) in enumerate(test_queries, 1):
        print(f"Query {i}: {desc}")
        print(f"  Input:  '{query}'")
        result = system.check_status(query)
        print(f"  Output: {result}\n")

    print("=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()