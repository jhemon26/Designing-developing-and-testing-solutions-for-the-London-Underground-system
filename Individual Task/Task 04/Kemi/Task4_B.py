from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
from generate_random_graph import generate_random_graph
import time
import pandas
from mst import get_total_weight
from dijkstra import dijkstra



#TASK B - Emperical Performance Measurement

#GENERATING THE ARTIFICAL NETWORK DATASETS

def core_stations_timer(graph):
    #A function that finds the time it takes to find the core network of a graph
    start = time.time()
    kruskal(graph)
    end = time.time()
    return end-start

#Make a function that finds the average time it takes to find the core station of a specific number of vertices
def average_calc(graph_vertices):
    #A function that finds the average time it takes to find the core stations of 10 graphs with the inputted vertices
    total_time = 0
    for y in range(10): #creating 10 random graphs with inputted number of vertices
        graph = generate_random_graph(graph_vertices, 0.2, directed= False, weighted=True)
        graph_time = core_stations_timer(graph) #Gets the time it takes to find the minimum spanning tree
        total_time += graph_time # increments the total with each time
    return total_time/10 #returns average time


def main():
    # begin = time.time()
    for x in range(100,1100,100):
        print(f"Average time {x} vertices: {average_calc(x)}")
    # end = time.time()
    # print("overall time: ", end-begin)

main()

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

mst_graph = tfl_kruskal_graph.get_edge_list() # an edge list of all the minimum edges needed (without the weights)

print(tfl_graph)
print(tfl_kruskal_graph)

#TOTAL JOURNEY TIME
total_weights = get_total_weight(tfl_kruskal_graph) # calculates the total weight of the core network graph
print(f"Total journey time of core train network: {int(total_weights)} minutes")

#REDUNDANT CONNECTIONS
original_edge_list = tfl_graph.get_edge_list()   # an edge list of all the original edges
new_edge_list =tfl_kruskal_graph.get_edge_list() # an edge list of all the minimum edges needed (without the weights)
redundant_edges = []
for x in original_edge_list:
    if x not in new_edge_list: # Finds edges that are in the original graph but not in the essential backbone graph
        redundant_edges.append(x) # Adds them to a list of redundant edges

print(redundant_edges)

#IMPACT ANALYSIS

# long journey -> Wimbledon -> Stratford
# find the shortest path between W and S






# for x in range(len(mst_graph)):
#     u, v = mst_graph[x][0], mst_graph[x][1] # changes the vertices from integers to the string labels (station name)
#     mst_graph[x] = (tfl_labels[u], tfl_labels[v])