# Task 1: Operational Station Status System
# Task 1a: Code Implementation and Verification
# Riyah Hussain

import os, sys

# -point Python at the CLRS folders-
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))           # /task 1
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)                        # /AdvancedADS
CLRS_ROOT = os.path.join(PROJECT_ROOT, "clrsPython")               # /AdvancedADS/clrsPython

# add CLRS subfolders so `from X import Y` works
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 11"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 10"))
sys.path.insert(0, os.path.join(CLRS_ROOT, "Chapter 31"))

# Now you can import
from chained_hashtable import ChainedHashTable
from hash_functions import hashpjw

class StationStatusTracker:
    """Track operational status of London Underground stations using chained hash table."""

    def __init__(self, table_size=11):
        """Initialize with hash table of given size (default: 11 for 5 stations)."""
        self.operational_stations = ChainedHashTable(table_size, hash_func=hashpjw)
        self.table_size = table_size
        self.station_count = 0

    def mark_operational(self, station_name):
        """Mark a station as operational. Returns True if added, False if already operational."""
        if self.is_operational(station_name):
            return False
        self.operational_stations.insert(station_name)
        self.station_count += 1
        return True

    def mark_closed(self, station_name):
        """Mark a station as closed. Returns True if removed, False if wasn't operational."""
        node = self.operational_stations.search(station_name)
        if node is None:
            return False
        self.operational_stations.delete(node)
        self.station_count -= 1
        return True

    def is_operational(self, station_name):
        """PRIMARY QUERY: Check if station is operational. Returns True/False."""
        result = self.operational_stations.search(station_name)
        return result is not None

    def get_status(self, station_name):
        """Get descriptive status text for a station."""
        if self.is_operational(station_name):
            return f"✓ {station_name} is OPERATIONAL"
        return f"✗ {station_name} is CLOSED"


# Demo and testing
if __name__ == "__main__":
    print("=" * 60)
    print("LONDON UNDERGROUND STATION STATUS TRACKER")
    print("Using Chained Hash Table with hashpjw hash function")
    print("=" * 60)

    tracker = StationStatusTracker()
    stations = ["A", "B", "C", "D", "E"]

    print("\nINITIALISATION")
    for station in stations:
        tracker.mark_operational(station)
    print(f"Added {len(stations)} stations as operational")

    print("\nPRIMARY QUERY TESTS: is_operational()")
    for station in ["A", "C", "E", "F"]:
        print(tracker.get_status(station))

    print("\nMAINTENANCE SIMULATION - Closing B and D")
    tracker.mark_closed("B")
    tracker.mark_closed("D")
    print(f"Operational stations remaining: {tracker.station_count}")

    print("\nSTATUS AFTER MAINTENANCE")
    print(tracker.get_status("B"))
    print(tracker.get_status("D"))
    print(tracker.get_status("A"))

    print("=" * 60)