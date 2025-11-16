from mst import kruskal
from generate_random_graph import generate_random_graph
import time


#TASK B - Empirical Performance Measurement

#GENERATING THE ARTIFICIAL NETWORK DATASETS

def core_stations_timer(graph):
    start = time.time()
    kruskal(graph)
    end = time.time()
    return end-start # returns time it takes to find the core network of a graph

def average_calc(graph_vertices):
    total_time = 0
    for y in range(5): #creating 5 random graphs with inputted number of vertices
        graph = generate_random_graph(graph_vertices, 0.05, directed= False, weighted=True)
        graph_time = core_stations_timer(graph) #Gets the time it takes to find the minimum spanning tree
        total_time += graph_time # increments the total with each time
    return total_time/5 #returns the average time

def main():
    for x in range(100,1100,100):
        print(f"Average time {x} vertices: {average_calc(x)}")

main()