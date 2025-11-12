
# @Jahid Hasan Emon                                                                              
# @SID : 001360753-7                                                                             
                                                                                                 
# Project    : Designing and Devoloping London Underorund Trains Map and Operations.             
# Task 3     : Journey Planner Based on Number of Stops                                          
# SubTask 3A : Empirical Performance Measurement

from adjacency_list_graph import AdjacencyListGraph   # Graph data structure (For Adjacency List)
from bfs import bfs                                   # BFS algorithm (For fewest stops search)
from print_path import print_path                     # For path reconstruction using BFS parent array

import csv             # CSV for Underground data file reading
import time            # Time for Exucution time measurement
import random          # Random for randomly selecting stations for performance evaluation



# Reads London Underground connections from CSV and builds a graph
def build_graph_from_csv(csv_filename):

    station_to_index = {}     # Maps station name -> integer Index (for BFS)
    index_to_station = []     # To reverse loolup index -> station name
    edge_list = []            # temporary storage of all edges befor we build the graph

    with open(csv_filename, encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # skip header row

        for row in reader:                # loop through every connection in the CSV
            #line = row[0].strip()        # can used later for line name if needed for Task 4
            s1 = row[1].strip()           # Get station1
            s2 = row[2].strip()           # Get station2

            if s1 == "" or s2 == "":      # handle empty values
                continue

            # Assign each new station a unique index number
            for station in (s1, s2):
                if station not in station_to_index:
                    station_to_index[station] = len(index_to_station)  # Assign next available index
                    index_to_station.append(station)    # Helps reverse lookup later
            # Store connection as tuple of (index1, index2)
            edge_list.append((station_to_index[s1], station_to_index[s2]))

    # Build a graph using number of stations detected and undirected edges
    G = AdjacencyListGraph(len(index_to_station), directed=False)

    # Insert each edge into graph, avoiding duplicates
    seen = set()                   
    for u, v in edge_list:                               # Loop through all edges
        if (u, v) not in seen and (v, u) not in seen:    # check for duplicates in undirected graph
            G.insert_edge(u, v)                          # Insert edge into graph
            seen.add((u, v))                             # We mark this edge as seen

    return G, station_to_index, index_to_station         # Return graph plus station lookup tables



# Uses BFS to compute the path and number of stops between two named stations   
def find_stops(G, station_to_index, index_to_station, start_name, end_name):

    start = station_to_index[start_name]           # Convert station name → integer index
    end = station_to_index[end_name]               # Convert destination name → integer index
    dist, parent = bfs(G, start)                   # Perform BFS and get distance and parent arrays

    # print_path reconstructs path using parent array From BFS
    path = print_path(parent, start, end, lambda i: index_to_station[i]) 

    print("\n-----------------------------------")
    print(f"Fewest stops from **{start_name}** to **{end_name}**:")
    print(" → ".join(path))
    print(f"Total stops: {dist[end]}")
    print("-----------------------------------\n")

    return dist[end]                               # Return number of stops


# Method that performs empirical timing tests of BFS on increasing network sizes
def empirical_test(G, station_to_index, index_to_station):

    stations = list(station_to_index.keys())  # Get full list of station names

    print("\n===== Empirical BFS Timing Results =====")

    for n in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
        if n > len(stations):
            break

        total_time = 0
        for _ in range(20):                          # repeat() times to make result accurate
            s1, s2 = random.sample(stations[:n], 2)  # randomly select two different stations from first n stations

            start_time = time.time()
            find_stops(G, station_to_index, index_to_station, s1, s2)
            total_time += (time.time() - start_time)

        avg_time = total_time / 50
        print(f"Network size n = {n} → Average BFS time: {avg_time:.6f} seconds")

csv_file = "Individual Task/Task 03/underground_edges.csv"
# Build full underground graph from CSV file
G, station_to_index, index_to_station = build_graph_from_csv(csv_file)

# Example test cases
find_stops(G, station_to_index, index_to_station, "Covent Garden", "Leicester Square")
find_stops(G, station_to_index, index_to_station, "Wimbledon", "Stratford")

# Check BFS Performance times empirically
empirical_test(G, station_to_index, index_to_station)