import sys # library for int_max

file = "input.txt"
file = "test.txt"

f = open(file, "r")
file_data = f.readlines()
f.close()

data = []
for row in file_data:
    data.append(row.strip())

class Graph():

    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = [[0 for column in range(vertices) for row in range(vertices)]]

    def printSolution(self, distance):
        print("Vertex \tDistance from Source")
        for node in range(self.vertices):
            print(node, "\t", distance[node])

    # a utility function to find the vertex with the minimum distance value
    # from the set of vertices not yet included in the shortest path tree
    def minDistance(self, distance, shortest_path_tree_set):
        # initialise minimum distance for next node
        min = sys.maxsize

        # search not nearest vertex not in the shortest path tree
        for node in range(self.vertices):
            if distance[node] < min and shortest_path_tree_set[node] == False:
                min = distance[node]
                min_index = node
        
        return min_index
    
    # function that implements D's single source shortest path algorithm for a
    # graph represented using adjacency matrix representation
    def dijkstra(self, source):
        distance = [sys.maxsize] * self.vertices
        distance[source] = 0
        shortest_path_tree_set = [False] * self.vertices

        for count in range(self.vertices):
            # pick the minimum distance vertex from the set of vertices not yet processed
            # x is always equal to source in first iteration
            x = self.minDistance(distance, shortest_path_tree_set)

            # put the minimum distance vertex in the shortest path tree
            shortest_path_tree_set[x] = True

            # update distance valye of the adjacent vertices of the picked vertx
            # only if the current distance is greater than the new distance
            # and the vertex is not in the shortest path tree
            for y in range(self.vertices):
                if self.graph[x][y] > 0 and shortest_path_tree_set[y] == False and distance[y] > distance[x] + self.graph[x][y]:
                    distance[y] = distance[x] + self.graph[x][y]

        self.printSolution(distance)

# Driver's code
if __name__ == "__main__":
    g = Graph(9)
    g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
               [4, 0, 8, 0, 0, 0, 0, 11, 0],
               [0, 8, 0, 7, 0, 4, 0, 0, 2],
               [0, 0, 7, 0, 9, 14, 0, 0, 0],
               [0, 0, 0, 9, 0, 10, 0, 0, 0],
               [0, 0, 4, 14, 10, 0, 2, 0, 0],
               [0, 0, 0, 0, 0, 2, 0, 1, 6],
               [8, 11, 0, 0, 0, 0, 1, 0, 7],
               [0, 0, 2, 0, 0, 0, 6, 7, 0]
               ]
 
    g.dijkstra(0)
        
