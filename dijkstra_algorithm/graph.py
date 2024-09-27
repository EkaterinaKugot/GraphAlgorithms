from node import Node
import heapq


class Graph:
    def __init__(self) -> None:
        self.nodes: dict = {}


    def get_node_by_name(self, name: str) -> Node:
        if not isinstance(name, str):
                raise TypeError("Неверный тип данных")

        return self.nodes.get(name, None)

    def add_node(self, node: Node):
        if not isinstance(node, Node):
                raise TypeError("Неверный тип данных")
        if node.name not in self.nodes.keys():
            self.nodes[node.name] = node

    def remove_node(self, node: Node):
        if not isinstance(node, Node):
                raise TypeError("Неверный тип данных")
        if node.name in self.nodes.keys():
            self.nodes.pop(node.name, None)

    def add_edge(self, begin: Node, end: Node, weight: float = 0.):
        if not isinstance(begin, Node) or not isinstance(end, Node):
                raise TypeError("Неверный тип данных")
        if not isinstance(weight, float):
                raise TypeError("Неверный тип данных")
        
        if begin in self.nodes.values() and end in self.nodes.values():
            begin.add_neighbour(end, weight)

    def remove_edge(self, begin: Node, end: Node):
        if not isinstance(begin, Node) or not isinstance(end, Node):
                raise TypeError("Неверный тип данных")
        
        if begin in self.nodes.values() and end in self.nodes.values():
            begin.remove_neighbour(end)
    
    def begin(self):
        return iter(self.nodes)

    def end(self):
        return iter(())
    
    def __repr__(self):
        string = "Graph("
        for node in self.nodes:
            string += node + ","
        string += ")"
        return string
    
    @staticmethod
    def load_from_file(file_path: str):
        if not isinstance(file_path, str) :
                raise TypeError("Неверный тип данных")
        graph = Graph()

        with open(file_path, 'r') as file:
            next(file)
            for line in file:
                source, target, weight = line.strip().split()
                weight = float(weight)

                source_node = graph.get_node_by_name(source)
                if source_node is None:
                    source_node = Node(source)
                    graph.add_node(source_node)

                target_node = graph.get_node_by_name(target)
                if target_node is None:
                    target_node = Node(target)
                    graph.add_node(target_node)

                graph.add_edge(source_node, target_node, weight)

        return graph
    
    def dijkstra(self, start: Node, target: Node):
        if not isinstance(start, Node) or not isinstance(target, Node):
            raise TypeError("Неверный тип данных")

        distances = {node: float('inf') for node in self.nodes.values()}
        distances[start] = 0

        passed = {node: None for node in self.nodes.values()}

        priority_queue = []
        heapq.heappush(priority_queue, (0, start))

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == target:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbour, weight in current_node.neighbours.items():
                distance = current_distance + weight

                if distance < distances[neighbour]:
                    distances[neighbour] = distance
                    passed[neighbour] = current_node
                    heapq.heappush(priority_queue, (distance, neighbour))

        path = []
        current = target
        while current is not None:
            path.append(current)
            current = passed[current]
        path.reverse()

        return path, distances[target]