# Author     : Anatolii Kvych                                                                         
# SID   : 001392532                                                                        
                                                                                                 
# Project    : Operational Station Status System             
# Task 4     : Analysis of the Core Network Backbone                                          
# SubTask 4A : Manual versus Code-Based Execution of a Core Network Algorithm
# Procedure:

# The network graph will look like this (weights in parentheses):
#
#        A(0)
#       /   \
#    B(1)    C(2)
#     | \    | \
#     |  D(3)  E(4)
#     |   /
#     D(3) - E(4)
#
# First we will have to list all edges with weights like follows:
#   A-B (4), A-C (2), B-C (1), etc.
# Then we have to sort edges by weight in ascending order to get the following list:
#   B-C (1), A-C (2), D-E (2), etc.
# After that we need to initialize MST as empty so that each vertex is its own component.
# Processing these edges in order will give us:
#   1) B-C (1): No cycle, add to MST
#   2) A-C (2): No cycle, add to MST
#   3) D-E (2): No cycle, add to MST
#   4) A-B (4): Would form a cycle (A-B-C-A), skip
#   5) B-D (5): Connects B-C-A component to D-E component, add to MST
#   6) C-D (8): Would form a cycle, skip
#   7) C-E (10): Would form a cycle, skip
# MST will be completed after adding N-1=4 edges.
# Finally, this fill give us MST (backbone) edges as follows:
#   B-C (1), A-C (2), D-E (2), B-D (5)
# And closable edges. Edges that arenot in MST):
#   A-B (4), C-D (8), C-E (10)
# In the end we will recieve two sets of edges:
# The essentialbackbone edges that cannot be closed without disconnecting stations and closable optional edges that can be temporarily closed during engineering works.


# Kruskal’s Algorithm will be implemented in main.py

# Importing nessesary modules
from mst import kruskal # Kruskal’s algorithm for computing MST
from adjacency_list_graph import AdjacencyListGraph # Graph data structure (adjacency list)

# Simple Dataset for testing

vertices = ['A', 'B', 'C', 'D', 'E']  # List of stations (nodes)
edges = [
    ('A', 'B', 4),  # Edge between A and B with weight 4
    ('A', 'C', 2),  # Edge between A and C with weight 2
    ('B', 'C', 1),  # Edge between B and C with weight 1
    ('B', 'D', 5),  # Edge between B and D with weight 5
    ('C', 'D', 8),  # Edge between C and D with weight 8
    ('C', 'E', 10), # Edge between C and E with weight 10
    ('D', 'E', 2)   # Edge between D and E with weight 2
]

# Building weighted and undirected graph
graph = AdjacencyListGraph(len(vertices), directed=False, weighted=True)

# Create a mapping from vertex names to indices for the graph (0-based indexing)
index = {v: i for i, v in enumerate(vertices)}

# Insert edges into the graph using the insert_edge() method
for u, v, w in edges:
    graph.insert_edge(index[u], index[v], w)

# Runs Kruskal algorithm and returns a graph representing the MST

# The kruskal() function returns a new graph representing the MST
mst_graph = kruskal(graph)

# Extracts MST edges (u, v)

# get_edge_list() returns a list of tuples (u_index, v_index)
mst_edges = mst_graph.get_edge_list()

# Prints results for backbone edges
print("\nTask 4A: The task is to find this maximum set of closable sections network that must be kept open.")
print("\nMST: Backbone edges that must be kept open:")
mst_set = set()  # To keep track of backbone edges for later

for u, v in mst_edges:
    # Lookup weight from the original graph
    w = graph.find_edge(u, v).get_weight()
    # Print using the original vertex names
    print(f"  {vertices[u]} -- {vertices[v]} (weight {w})")
    # Store edges as sorted tuples for easy comparison later
    mst_set.add(tuple(sorted((vertices[u], vertices[v]))))


# Compute closable edges (edges not in the MST)

# Original edges stored as sorted tuples
original_set = {tuple(sorted((u, v))) for u, v, w in edges}
# Edges that are not in the MST are closable
closable = original_set - mst_set

print("\nMST: Closable edges that can be temporarily closed:")
for u, v in closable:
    # Lookup weight from original edges for display
    w = next(w for x, y, w in edges if {x, y} == {u, v})
    print(f"  {u} -- {v} (weight {w})")

