# Jonathan Copete Ordonez
# ID - 000980359-9
#Task 2a: Shortest journey time on a small artificial network (A–F)
# Graph: undirected, weighted (minutes)
#Expected output: A -> B -> C -> D -> F, Total 9 minute

from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

labels = ['A','B','C','D','E','F']
idx = {v:i for i,v in enumerate(labels)}
G = AdjacencyListGraph(len(labels), True, True)  # directed=True, weighted=True

edges = [
    ('A','B',2), ('A','C',4),
    ('B','C',1),
    ('C','D',4), ('C','E',5), ('C','F',8),
    ('D','F',2),
    ('E','F',2),
]
for u,v,w in edges:  # undirected => add both directions
    G.insert_edge(idx[u], idx[v], w)
    G.insert_edge(idx[v], idx[u], w)

d, pi = dijkstra(G, idx['A'])

# reconstruct A->F
path, v = [], idx['F']
while v is not None and v != -1:
    path.append(labels[v]); v = pi[v]
print("Shortest path:", " -> ".join(reversed(path)))
print("Total time:", d[idx['F']], "minutes")