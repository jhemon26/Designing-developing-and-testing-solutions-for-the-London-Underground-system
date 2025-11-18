# Jonathan Copete Ordonez
# ID - 000980359-9
#Task 2a: Shortest journey time on a small artificial network (A–F)
# Graph: undirected, weighted (minutes)
#Expected output: A -> B -> C -> D -> F, Total 9 minute


import os
import sys

here = os.path.dirname(__file__)

sys.path.append(here)

for name in os.listdir(here):
    path = os.path.join(here, name)
    if os.path.isdir(path):
        sys.path.append(path)

from dijkstra import dijkstra
from adjacency_list_graph import AdjacencyListGraph

stations = ["A", "B", "C", "D", "E", "F"]

edges = [
    ("A", "B", 2),
    ("A", "C", 4),
    ("B", "C", 1),
    ("C", "D", 4),
    ("C", "E", 5),
    ("C", "F", 8),
    ("D", "F", 2),
    ("E", "F", 2),
]

G = AdjacencyListGraph(card_V=len(stations), directed=False, weighted=True)


for u_name, v_name, w in edges:
    u = stations.index(u_name)
    v = stations.index(v_name)
    G.insert_edge(u, v, w)

start_label = "A"
end_label = "F"

s = stations.index(start_label)
t = stations.index(end_label)

d, pi = dijkstra(G, s)

path_indices = []
v = t
while True:
    path_indices.append(v)

    if v == s or pi[v] is None:
        break
    v = pi[v]

path_indices.reverse()
path_stations = [stations[i] for i in path_indices]

print(
    f"The shortest path from A-F is {d[t]} minutes & this is the station it has passed: "
    + " -> ".join(path_stations)
)
