
# @Jahid Hasan Emon
# @SID : 001360753-7

# Project    : Designing and Devoloping London Underorund Trains Map and Operations.
# Task 3     : Journey Planner Based on Number of Stops
# SubTask 3A : Manual code exicution first (Demo Code)

""" 
Procedure :
We first create an undirected graph data structure and store the station 
connections in a dictionary where each key represents a station node 
and the value represents its directly connected neighboring stations.
The London Underground network is represented as: 
                0
               /  \
             1     4
           /|     /  \
        2   3   5     6
                      \
                       7
We store the connections as: {0: [1, 4], 1: [0, 2, 3], 4: [0, 5, 6], ...}
where each connection is bidirectional.
We will perform Breadth-First Search (BFS) using a Queue to find the shortest path
We will have VisitedNodes to track explored stations (a bool array)
"QUEUE" to process stations one by one. "Parent" to reconstruct the path later.
We have startNode and endNode as start and end stations.

"""


from fifo_queue import Queue                           # Import CLRS Queue class 
from adjacency_list_graph import AdjacencyListGraph    # Importing Adjacency List Graph class

class LUGW:
    def __init__(self, num1, num2):                    # For initializing start and end nodes
        self.num1 = num1
        self.num2 = num2

        
        self.connections = {       # Here K:V is Station : Connections 
            0: [1, 4],             
            1: [0, 2, 3],          
            2: [1],        
            4: [0, 5, 6],  
            5: [4],        
            3: [1],               
            6: [4, 7],     
            7: [6]         
        }

    def shortest_path(self):                        # Method to find shortest path using BFS
        
        startNode, endNode = self.num1, self.num2   # Initialize start and end nodes

        if startNode == endNode:                    # If start and end nodes are the same
            return [startNode], 0                   # WE return the start node and means 0 stops

        
        stations = AdjacencyListGraph(8, directed=False)      # UnDirected graph with 8 stations value 

        for station, neighbors in self.connections.items():   # for each station and its neighbors                                                   
            for neighbor in neighbors:                        # we search for neighbors 
                if not stations.has_edge(station, neighbor):  # If we dont find and edge then, 
                    stations.insert_edge(station, neighbor)   # We insert an edge between station and neighbor


        queue = Queue(stations.get_card_V())                 # Initialize the queue
        queue.enqueue(startNode)                             # We Enqueue the first/start node)
        visitedNodes = [False] * stations.get_card_V()       # Initialize visited nodes array as False 
        
        visitedNodes[startNode] = True                       # Mark start node as visited 
        parent = [None] * stations.get_card_V()              # Initialized parent array to reconstruct path later

        while not queue.is_empty():                          # we Check while queue is not empty
            currentNode = queue.dequeue()                    # if not empty then we dequeue the front element
            
            
            for edge in stations.get_adj_list(currentNode):  # check all adjacent edges of current node
                node = edge.get_v()                          
                
                if visitedNodes[node]:  # if already visited then skip and continue 
                    continue
            
                visitedNodes[node] = True   # Else mark visited and assign it as child of current node
                parent[node] = currentNode  # Set parent of node to currentNode for path reconstruction.
                queue.enqueue(node)         # We enqueue the node for further exploration

                
                if node == endNode:                   # If we reach endnode then we reconstruct the path
                    path = [endNode]                  
                    while path[-1] != startNode:      # while last element is not startnode then
                        path.append(parent[path[-1]]) # we keep appending the parent node 
                    path.reverse()                    # we reverse the path to get from start to end
                    return path, len(path) - 1        # return the path and number of stops

        return None, -1  


if __name__ == "__main__":                # Main func to take user input and display output
    try:
        num1 = int(input("\nPlease enter the starting station number (0-7): "))
        num2 = int(input("Please enter the destination station number (0-7): "))
    except ValueError:
        print("Invalid input. Type the station number again between 0-7")
    else:
        journeyPlanner = LUGW(num1, num2)
        path, stops = journeyPlanner.shortest_path()   # Calling shortest_path method
        if path is None:
            print(f"No path found between {num1} and {num2}.")
        else:
            print(f"The shortest path between stations is {path} and number of stops is {stops}.")