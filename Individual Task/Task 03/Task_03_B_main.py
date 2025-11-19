
# @Jahid Hasan Emon                                                                              
# @SID : 001360753-7                                                                             
                                                                                                 
# Project    : Designing and Devoloping London Underorund Trains Map and Operations.             
# Task 3     : Journey Planner Based on Number of Stops                                          
# SubTask 3A : Empirical Performance Measurement and Artificial BFS Timing


from adjacency_list_graph import AdjacencyListGraph   # Graph data structure (For Adjacency List)
from bfs import bfs                                   # BFS algorithm (For fewest stops search)
from print_path import print_path                     # For path reconstruction using BFS parent array

import csv             # CSV for Underground data file reading
import time            # Time for Exucution time measurement
import random          # Random for randomly selecting stations for performance evaluation
import matplotlib.pyplot as plt    # at the very top of your file

artificial_results = []            # To store Artificial BFS timing results
empirical_results =  []            # To store Empirical BFS timing results



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
        if (u, v) not in seen and (v, u) not in seen:    # Check for duplicates in undirected graph
            G.insert_edge(u, v)                          # Insert edge into graph
            seen.add((u, v))                             # We mark this edge as seen

    return G, station_to_index, index_to_station         # Return graph plus station lookup tables


# Method that performs artificial timing tests of BFS on randomly generated graphs
def artificial_test():
    print("\n===== Artificial BFS Timing Results =====")
    for n in [100, 200, 400, 600, 800, 1000, 2000, 3000, 4000, 5000]:         # Different network sizes
        G = AdjacencyListGraph(n, directed=False)     # Create empty undirected graph with n nodes

        for i in range(n):
            for _ in range(3):                        # Each node connects to 3 random other nodes
                j = random.randint(0, n - 1)
                if j != i and not G.has_edge(i, j):   # Avoid self-loops and duplicate edges
                    G.insert_edge(i, j)

        total = 0
        for _ in range(20):
            s1, s2 = random.sample(range(n), 2)      # Randomly select two different nodes
            t0 = time.time()
            bfs(G, s1)
            total += time.time() - t0                # Accumulate BFS time

        avg_time = total / 20
        print(f"n={n} → avg BFS time = {avg_time:.6f} sec")

        artificial_results.append((n, avg_time))   # We store results for plotting later



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
        for _ in range(20):                          # Repeat() times to make result accurate
            s1, s2 = random.sample(stations[:n], 2)  # Randomly select two different stations from first n stations 
            start_idx = station_to_index[s1]         # Convert start station to index
            t0 = time.time()
            bfs(G, start_idx)                        # We run BFS
            total_time += (time.time() - t0)

        avg_time = total_time / 20                   # Avarage times per BFS
        print(f"Network size n = {n} → Average BFS time: {avg_time:.6f} seconds")
        


# Method to plot Artificial results
def plot_artificial_results():                                    
    if not artificial_results:
        print("No empirical results to plot.")
        return

    ns = [x[0] for x in artificial_results]           # Extract network sizes
    times = [x[1] for x in artificial_results]        # Extract times
    plt.plot(ns, times, marker="o")                  # Plot with circle markers
    plt.xlabel("Network Size (n)")
    plt.ylabel("Average BFS Time (seconds)")
    plt.title("BFS Performance on London Underground Network")
    plt.grid(True)
    plt.show()

csv_file = "Individual Task/Task 03/underground_edges.csv"
# Build full underground graph from CSV file
G, station_to_index, index_to_station = build_graph_from_csv(csv_file)
# Example test cases
find_stops(G, station_to_index, index_to_station, "Covent Garden", "Leicester Square")
find_stops(G, station_to_index, index_to_station, "Wimbledon", "Stratford")

artificial_test()  # To check the Artificial network timing 
empirical_test(G, station_to_index, index_to_station)  # Check BFS Performance times empirically
plot_artificial_results()  # Plot the Artificial Graph

#For upload 