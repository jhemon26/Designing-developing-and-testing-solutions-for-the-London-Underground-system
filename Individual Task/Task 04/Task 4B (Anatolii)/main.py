# Author     : Anatolii Kvych                                                                         
# SID   : 001392532                                                                        
                                                                                                 
# Project    : Operational Station Status System             
# Task 4     : Analysis of the Core Network Backbone                                          
# SubTask 4B : Empirical Measurement and Application

# Importing nessesary modules
import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
import heapq
import random
import time
import matplotlib.pyplot as plt


#Loading Excel file

excel_file = "Individual Task/Task 04/Task 4B (Anatolii)/london_underground_data.xlsx"
df = pd.read_excel(excel_file, header=None)
edges_df = df.dropna(subset=[1, 2, 3])


# Removing duplicates (undirected edges)

unique_edges = {}
for _, row in edges_df.iterrows():
    u = row[1]
    v = row[2]
    w = int(row[3])
    key = tuple(sorted((u, v)))
    if key not in unique_edges or w < unique_edges[key]:
        unique_edges[key] = w

edges = [(u, v, w) for (u, v), w in unique_edges.items()]

# Extract vertices

vertices = sorted(set([u for u, v, w in edges] + [v for u, v, w in edges]))
index = {v: i for i, v in enumerate(vertices)}

# Building weighted, undirected graph

graph = AdjacencyListGraph(len(vertices), directed=False, weighted=True)
for u, v, w in edges:
    if not graph.has_edge(index[u], index[v]):
        graph.insert_edge(index[u], index[v], w)

# Computing MST backbone

mst_graph = kruskal(graph)
mst_edges = mst_graph.get_edge_list()

mst_set = set()
for u, v in mst_edges:
    mst_set.add(tuple(sorted((vertices[u], vertices[v]))))

# Redundant edges
original_set = {tuple(sorted((u, v))) for u, v, w in edges}
closable = original_set - mst_set

total_weight = sum(graph.find_edge(index[u], index[v]).get_weight() for u, v in mst_set)

print(f"\nTotal backbone weight: {total_weight}\n")
print("Sample of 10 redundant (closable) edges:")
for i, (u, v) in enumerate(list(closable)[:10]):
    w = graph.find_edge(index[u], index[v]).get_weight()
    print(f"{u} - {v} (weight {w})")


# Dijkstra shortest path for (impact analysis)


def dijkstra(graph, index, source):
    n = graph.get_card_V()
    dist = [float('inf')] * n
    prev = [None] * n
    dist[index[source]] = 0
    visited = [False] * n
    heap = [(0, index[source])]
    
    while heap:
            d, u = heapq.heappop(heap)
            if visited[u]:
                continue
            visited[u] = True
            for edge in graph.get_adj_list(u):
                v = edge.get_v()
                w = edge.get_weight()
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    heapq.heappush(heap, (dist[v], v))
    return dist, prev

def reconstruct_path(prev, index, source, target):
    path = []
    u = index[target]
    while u is not None:
        path.append(u)
        u = prev[u]
    path.reverse()
    return path

# (Impact analysis example)
source_station = "Baker Street"
target_station = "Elephant & Castle"

dist_orig, prev_orig = dijkstra(graph, index, source_station)
path_orig_indices = reconstruct_path(prev_orig, index, source_station, target_station)
path_orig = [vertices[i] for i in path_orig_indices]
time_orig = dist_orig[index[target_station]]

backbone_graph = AdjacencyListGraph(len(vertices), directed=False, weighted=True)
for u, v in mst_set:
    w = graph.find_edge(index[u], index[v]).get_weight()
    backbone_graph.insert_edge(index[u], index[v], w)

dist_back, prev_back = dijkstra(backbone_graph, index, source_station)
path_back_indices = reconstruct_path(prev_back, index, source_station, target_station)
path_back = [vertices[i] for i in path_back_indices]
time_back = dist_back[index[target_station]]

print(f"\nJourney from {source_station} to {target_station}:")
print(f"Original path: {path_orig} | Total time: {time_orig}")
print(f"Backbone-only path: {path_back} | Total time: {time_back}")
print(f"Difference in journey time: {time_back - time_orig}")


# Empirical Performance Measurement
# Generate a random weighted undirected graph with n vertices
def generate_random_graph(n, edge_prob=0.05, max_weight=10):
    g = AdjacencyListGraph(n, directed=False, weighted=True)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_prob:  # probability of having an edge
                w = random.randint(1, max_weight)
                g.insert_edge(u, v, w)
    return g

network_sizes = list(range(100, 1001, 100))
avg_times = []

for n in network_sizes:
    times = []
    # Run 5 times per size and average
    for _ in range(5):
        random_graph = generate_random_graph(n, edge_prob=0.05)
        start_time = time.time()
        kruskal(random_graph)
        times.append(time.time() - start_time)
    avg_times.append(sum(times)/len(times))
    print(f"n={n}, avg MST calculation time: {avg_times[-1]:.4f} sec")

# Plot performance graph
plt.figure(figsize=(8,5))
plt.plot(network_sizes, avg_times, marker='o', color='blue')
plt.title("Empirical MST calculation time vs network size")
plt.xlabel("Number of stations (n)")
plt.ylabel("Average MST calculation time (seconds)")
plt.grid(True)
plt.show()