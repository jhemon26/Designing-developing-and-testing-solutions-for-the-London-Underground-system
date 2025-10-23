
# @Jahdi Hasan Emon
# @SID : 001360753-7

# Project    : Designing and Devoloping London Underorund Trains Map and Operations.
# Task 3     : Journey Planner Based on Number of Stops
# SubTask 3A : Manual code exicution first (Demo Code)

"""
Procedure :
We first create a Tree based Data structuer and then we store the data in a Dict so that, we can
use the key as nodes and neighbours as the value. 
                0
               /  \
             1     4
           /|     /  \
        2   3   5     6
                      \
                       7
So here we store  dict { K:V} as {0 : [2,3], 2: [4,5]} and so on.
WE, perform BFS search here and use QUEUE.
we would have Root, visited, queue.
Where, root is start node and visited will be a sete() to keep tract of seen nodes
queue will be used to define the relationship and levels of BFS. 
"""

from collections import deque

class LUGW:
    def __init__ (self, num1, num2):
        self.num1 = num1
        self.num2 = num2


        self.stations = { 0:[1,4],   # Storing the graph as a dictionary 
              1:[0,2,3] ,            # Here k is node and v is connection
              2:[1],  
              4:[0,5,6], 
              5:[4], 3:[1],         
              6:[4,7], 7:[6] }



    def shortest_path (self):                      # Method to find the shortest path 
        
        startNode, endNode = self.num1, self.num2  # Assigning start and end nodes

        if startNode == endNode: 
            return [startNode], 0

        queue = deque([startNode])   # Initializing the queue with a start node 
        visitedNodes = {startNode}   # Used set to keep track of visited nodes (rmv dplcts)
        parent = {}                  # To keep track of parent node for path reconstruction 

        while queue:                 
            currentNode = queue.popleft()  # Dequeuing the first node
            for node in self.stations.get(currentNode, []): # checking neighbours of current node
                if node in visitedNodes:   # If curntnd already visited then ignore
                    continue
                
                visitedNodes.add(node)      # if not then we mark it visited
                parent[node] = currentNode  # also we set the parent of this node 
                queue.append(node)          # We enqueue the node for from the queue

                if node == endNode:
                    path = [endNode]        # If the node is enddNode then we reconstruct the path 
                    while path[-1] != startNode:   # We start from end to start to get the path
                        path.append(parent[path[-1]])  # WE keep appending the parent node
                    path.reverse()                     # WE reverse to get the path from start to end
              
                    return path, len(path) - 1    # Retuning the path and number of stops
        return None, -1                           # If no path then return None                     
        
    
if __name__ == "__main__":                  # Main func to get user input and display output
    try:
      num1 = int(input("\nPlease enter the starting station number (0-7): "))
      num2 = int(input("Please enter the destination station number (0-7): "))
    except ValueError:
        print ("Invalid input. Type the station number again between 0-7")
    else:
        journeyPlanner = LUGW(num1, num2)
        path, stops = journeyPlanner.shortest_path()
        if path is None:
            print (f"No path found between {num1} and {num2}. ")
        else:
            print (f"The shortest path between station is {path} and number of stops is {stops}.")
