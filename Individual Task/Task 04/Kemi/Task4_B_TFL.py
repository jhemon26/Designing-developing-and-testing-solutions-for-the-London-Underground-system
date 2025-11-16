from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal, get_total_weight
import pandas
from dijkstra import dijkstra

#TASK B - Application with London Underground Data

#CORE BACKBONE CALCULATION
tfl_data = pandas.read_excel("London Underground data.xlsx")
tfl_lst = tfl_data.values.tolist()

def create_edge_labels(data_list):
    edge_dict = {}
    labels = []
    for edge in range(len(data_list)):
        vertices1,vertices2,weight = data_list[edge][1],data_list[edge][2],data_list[edge][3]
        if vertices1 not in labels: #Adding all the stations names to a label list
            labels.append(vertices1)
        if type(vertices1) == str and type(vertices2) == str and type(weight) == float: # Checks to see if the edge has all it's required information
                edge_keys = edge_dict.keys() # Gets all the connections currently stored in the dictionary
                if (vertices1,vertices2) and (vertices2,vertices1) not in edge_keys: # This prevents duplicate station connections
                    edge_dict[(vertices1,vertices2)] = weight
    return edge_dict,labels

tfl_edge_dict,tfl_labels = create_edge_labels(tfl_lst)

#MAKING THE TFL GRAPH
tfl_graph = AdjacencyListGraph(len(tfl_labels), False, True) #Undirected #Weighted
for x in tfl_edge_dict: #inserting the all stations edges/connections and its times into the graph
    tfl_graph.insert_edge(tfl_labels.index(x[0]),tfl_labels.index(x[1]), tfl_edge_dict[x])

tfl_kruskal_graph = kruskal(tfl_graph) # this finds the minimum spanning tree of a graph


#TOTAL JOURNEY TIME
total_weights = get_total_weight(tfl_kruskal_graph) # calculates the total weight of the core network graph
print(f"Total journey time of core train network: {int(total_weights)} minutes")


#REDUNDANT CONNECTIONS
original_edge_list = tfl_graph.get_edge_list()   # an edge list of all the original edges
new_edge_list = tfl_kruskal_graph.get_edge_list() # an edge list of all the minimum edges needed (without the weights)
redundant_edges = []
print("\nRedundant Edges:")
for x in original_edge_list:
    if x not in new_edge_list: # Finds edges that are in the original graph but not in the essential backbone graph
        redundant_edges.append(x) # Adds them to a list of redundant edges
        print(f"{tfl_labels[x[0]]} and {tfl_labels[x[1]]}")

#IMPACT ANALYSIS
directed_tfl_graph = AdjacencyListGraph(len(tfl_labels), True, True)

source = tfl_labels.index("Stratford")
destination = tfl_labels.index("South Wimbledon")

def insert_graph(edge_list,labels, graph, weights= True):
    if weights is False:
        for i in edge_list:
            u, v = i[0], i[1]
            weight = tfl_graph.find_edge(u, v).get_weight()
            graph.insert_edge(u, v, weight)
            graph.insert_edge(v, u, weight)
    else:
        for z in edge_list:
            graph.insert_edge(labels.index(z[0]), labels.index(z[1]), edge_list[z])
            graph.insert_edge(labels.index(z[1]), labels.index(z[0]), edge_list[z])
insert_graph(tfl_edge_dict, tfl_labels, directed_tfl_graph)

# Long journey -> South Wimbledon -> Stratford

d, pi = dijkstra(directed_tfl_graph,source)

def path_constructor(vertex, path_list, edge_list, predecessor_list):
    while vertex is not None:
        path_list.append(tfl_labels[vertex]) #Adds the name of the station to the path list
        edge_list.append((vertex,predecessor_list[vertex]))
        vertex = predecessor_list[vertex] #the new V is the index of the previous station
    return path_list, edge_list

path,path_edge_list = path_constructor(destination,[],[],pi)

print(f"\nJourney from Stratford to South Wimbledon\n{' -> '.join(reversed(path))}")
print("Total journey time: ",d[destination])

for x in path_edge_list:
    if x in redundant_edges: #Checks if the path has any redundant edges (not essential edges)
        print(f"Yes, the {tfl_labels[x[0]]} and {tfl_labels[x[1]]} connection is part of the redundant connection.")

#FIND THE PATH ON BACKBONE NETWORK
directed_tfl_kruskal_graph = AdjacencyListGraph(len(tfl_labels), True, True)
insert_graph(new_edge_list,tfl_labels,directed_tfl_kruskal_graph,weights=False)
kruskal_d, kruskal_pi = dijkstra(directed_tfl_kruskal_graph, source)
k_path, k_edges = path_constructor(destination,[],[],kruskal_pi)

print(f"\nJourney from Stratford to South Wimbledon on the Core Network:\n{' -> '.join(reversed(k_path))}")
print("Total journey time: ",kruskal_d[destination])
