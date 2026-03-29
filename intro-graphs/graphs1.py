class Graph:
    def __init__(self):
        self.graph = {}
    def add_vertex(self,vertex):
        self.graph[vertex] = []
    def add_edge(self,vertex1,vertex2):
        self.graph[vertex1].append(vertex2)
        self.graph[vertex2].append(vertex1)
    def display(self):
        print(self.graph)
    def bfs(self,start):
        queue = [start]
        visited = set([])
        while len(queue) > 0:
            node = queue[0]
            queue = queue[1:]
            if node not in visited:
                visited.add(node)
            items = self.graph[node]
            items_help = [i for i in items if i not in visited]
            queue.extend(items_help)
        return(visited)



g = Graph()
g.add_vertex("A")
g.add_vertex("B")
g.add_vertex("C")
g.add_vertex("D")
g.add_edge("A", "B")
g.add_edge("A", "C")
g.add_edge("B", "D")
g.display()
print(g.bfs("A"))  # should visit A, B, C, D