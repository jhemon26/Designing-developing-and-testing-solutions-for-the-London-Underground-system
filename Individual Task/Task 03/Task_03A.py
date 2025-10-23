
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
             2     3
           /|     /  \
        4   5   6     7
So here we store  dict { K:V} as {0 : [2,3], 2: [4,5]} and so on.
WE, perform BFS search here and use QUEUE.
we would have Root, visited, queue.
Where, root is start node and visited will be a sete() to keep tract of seen nodes
queue will be used to define the relationship and levels of BFS. 
"""


stations = { 0:[2,3], 2:[4,5], 
            4:[2], 5:[2], 3:[0,6,7],
            6:[3], 7:[3] }





class LUGW:
    def __init__ (self, num1, num2):
        self.num1 = num1
        self.num2 = num2





    def shortest_path (self):
        visitedNodes = set()
    
