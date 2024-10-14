import random
from src.graph import Graph
from src.node import Node


class Ant:
    def __init__(self, graph: Graph):
        if not isinstance(graph, Graph):
                raise TypeError("Неверный тип данных")
        
        self.graph = graph
        self.current_node = None
        self.tour = []
        self.total_distance = 0.0

    # Посещение узла муравьем
    def visit_node(self, node: Node) -> None:
        if not isinstance(node, Node):
                raise TypeError("Неверный тип данных")
        
        if self.current_node:
            weight = self.current_node.neighbours[node]
            self.total_distance += weight
        self.tour.append(node)
        self.current_node = node

    # Выбрать следующий узел из соседей
    def choose_next_node(self, a: float, b: float) -> Node:
        if not isinstance(a, float) or not isinstance(b, float):
                raise TypeError("Неверный тип данных")
        
        if not self.current_node:
            return random.choice(list(self.graph.nodes.values()))

        neighbours = list(self.current_node.neighbours.keys())
        # Убираем уже посещенные узлы из соседей
        unvisited_neighbours = [n for n in neighbours if n not in self.tour]
        
        if not unvisited_neighbours:
            return None  # Все узлы посещены
        
        total_probability = 0.0
        probabilities = []

        for neighbour in unvisited_neighbours:
            pheromone_level = self.graph.get_pheromone_level(self.current_node, neighbour) # rij
            distance = self.current_node.neighbours[neighbour] # dij - вес ребра мужде узлами i и j 
            attractiveness = 1 / distance  # Привлекательность nij, как 1/dij
            
            probability = (pheromone_level ** a) * (attractiveness ** b) # (rij^a) * (nij^b)
            probabilities.append(probability)
            total_probability += probability # Е((rij^a)*(nij^b))

        # pij = (rij^a) * (nij^b) / Е((rij^a) * (nij^b))
        probabilities = [p / total_probability for p in probabilities]
        
        return random.choices(unvisited_neighbours, weights=probabilities)[0]