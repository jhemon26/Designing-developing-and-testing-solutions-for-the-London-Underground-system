#Task 4 A - Finding the minimum amount of open stations required across an artificial network (U, V, W, X, Y, Z)

#Expected outcome: UV -> VW -> VX -> XZ -> YZ

from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
# from print_path import print_path

labels = ['U','V','W','X','Y','Z'] #names of the vertices

station_array_edges = [
    ("U","V", 1), ("U","W", 4),
    ("V","X", 2), ("V","W", 1),       #list of all the edges and it's weights
    ("W","Y", 5), ("W", "X", 4),
    ("X","Z", 3),
    ("Y","Z", 2),
]

station_graph = AdjacencyListGraph(6, False, True)

for x,y,z in station_array_edges:
    station_graph.insert_edge(labels.index(x),labels.index(y), z)   # This adds the vertices of the edge and the weight to the graph

station_kruksal = kruskal(station_graph) # This finds the minimum spanning tree of a graph

mst_graph = station_kruksal.get_edge_list() # An edge list of all the minimum edges needed (without the weights)

for x in range(len(mst_graph)):
    u, v = mst_graph[x][0], mst_graph[x][1] # Changes the vertices from integers to the string labels (station name)
    mst_graph[x] = (labels[u], labels[v])

print(mst_graph)


