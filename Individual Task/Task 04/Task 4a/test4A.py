from merge_sort import merge_sort
from adjacency_list_graph import AdjacencyListGraph
from disjoint_set_forest import make_set, find_set, union
from min_heap_priority_queue import MinHeapPriorityQueue


class KruskalEdge:
    def __init__(self, u, v, weight=None):
        """Initialize edge class that contains both endpoints and weight."""
        self.u = u
        self.v = v
        if weight is not None:
            self.weight = weight

    def get_u(self):
        """Return endpoint of vertex that edge starts."""
        return self.u

    def get_v(self):
        """Return endpoint of vertex that edge ends."""
        return self.v

    def get_weight(self):
        """Return weight of edge."""
        return self.weight

    def __le__(self, edge2):
        """Compare weights for less than or equal to."""
        return self.weight <= edge2.weight

    def __str__(self):
        """Print edge with endpoints and weight."""
        return f"({self.u}, {self.v}), weight: {self.weight}"


def kruskal(G):
    """Return the minimum spanning tree of a weighted, undirected graph G using Kruskal's algorithm."""
    if G.is_directed():
        raise RuntimeError("Graph should be undirected.")

    card_V = G.get_card_V()
    mst = AdjacencyListGraph(card_V, False, True)
    forest = [None] * card_V
    for v in range(card_V):
        forest[v] = make_set(v)

    edges = []
    for u in range(card_V):
        for edge in G.get_adj_list(u):
            if u < edge.get_v():
                edges.append(KruskalEdge(u, edge.get_v(), edge.get_weight()))
    merge_sort(edges)

    for edge in edges:
        u = forest[edge.get_u()]
        v = forest[edge.get_v()]
        if find_set(u) != find_set(v):
            mst.insert_edge(edge.get_u(), edge.get_v(), edge.get_weight())
            union(u, v)

    return mst


def print_undirected_edges(G, vertices):
    """Print the edges in an undirected graph G."""
    for u in range(G.get_card_V()):
        for edge in G.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                print(f"({vertices[u]}, {vertices[v]})")


def find_removable_edges(G, mst):
    """Identify and print removable edges that are not in the MST but keep the graph connected."""
    removable_edges = []
    for u in range(G.get_card_V()):
        for edge in G.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                if not mst.has_edge(u, v):
                    removable_edges.append((u, v, edge.get_weight()))
    return removable_edges


# Modified Testing
if __name__ == "__main__":
    import numpy as np
    from generate_random_graph import generate_random_graph

    # Example London Underground graph (substitute with actual station data)
    # Use a smaller set of 5 stations
    vertices = ['Oxford Circus', 'Baker Street', 'Piccadilly Circus', 'Waterloo', 'Green Park']

    # Define edges with station names and sample weights
    edges = [
        ('Oxford Circus', 'Baker Street', 4),
        ('Oxford Circus', 'Green Park', 8),
        ('Baker Street', 'Piccadilly Circus', 8),
        ('Piccadilly Circus', 'Waterloo', 7),
        ('Green Park', 'Waterloo', 6)
    ]

    graph1 = AdjacencyListGraph(len(vertices), False, True)
    for edge in edges:
        graph1.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]), edge[2])

    # Generate MST using Kruskal's algorithm
    print("Generating MST using Kruskal's algorithm:")
    kruskal_mst = kruskal(graph1)

    # List edges in the MST
    print("Edges in the MST:")
    print_undirected_edges(kruskal_mst, vertices)

    # Identify removable edges
    removable_edges = find_removable_edges(graph1, kruskal_mst)
    print("\nRemovable edges (keeping graph connected):")
    for u, v, weight in removable_edges:
        print(f"{vertices[u]} -- {vertices[v]}, weight: {weight}")
