import random
from src.graph import Graph
from src.node import Node


class Ant:
    def __init__(self, graph: Graph, greedy: bool = False):
        if not isinstance(graph, Graph) or not isinstance(greedy, bool):
                raise TypeError("Неверный тип данных")
        
        self.graph = graph
        self.current_node = None
        self.tour = []
        self.total_distance = 0.0
        self.amount_pheromones = 0
        self.greedy = greedy

    # Посещение узла муравьем
    def visit_node(self, node: Node) -> None:
        if not isinstance(node, Node):
                raise TypeError("Неверный тип данных")
        
        if self.current_node:
            weight = self.current_node.neighbours[node]
            self.total_distance += weight
        self.tour.append(node)
        self.current_node = node
    
    def update_amount_pheromones(self, begin: Node, end: Node):
        self.amount_pheromones += self.graph.get_pheromone_level(begin, end)

    # Выбрать следующий узел из соседей
    def choose_next_node(self, a: float, b: float) -> Node:
        if not isinstance(a, float) or not isinstance(b, float):
                raise TypeError("Неверный тип данных")
        
        if not self.current_node:
            return random.choice(list(self.graph.nodes.values()))

        
        
        if not self.greedy: # Обычный муравей
            neighbours = list(self.current_node.neighbours.keys())
            # Убираем уже посещенные узлы из соседей
            unvisited_neighbours = [n for n in neighbours if n not in self.tour]
            
            if not unvisited_neighbours:
                return None  # Все узлы посещены
        
            probabilities = []

            for neighbour in unvisited_neighbours:
                pheromone_level = self.graph.get_pheromone_level(self.current_node, neighbour) # rij
                distance = self.current_node.neighbours[neighbour] # dij - вес ребра мужде узлами i и j 
                if distance == 0:
                    attractiveness = 1 + 0.000001
                else:
                    attractiveness = 1 / distance  # Привлекательность nij, как 1/dij
                
                probability = (pheromone_level ** a) * (attractiveness ** b) # (rij^a) * (nij^b)
                probabilities.append(probability)
            
            next_node = random.choices(unvisited_neighbours, weights=probabilities)[0]
            return next_node
        else: # Жадный муравей
            # Убираем уже посещенные узлы из соседей
            unvisited_neighbours = {k:v for k, v in self.current_node.neighbours.items() if k not in self.tour} 

            if not unvisited_neighbours:
                return None  # Все узлы посещены

            # Выбираем узел с минимальной дистанцией
            min_neighbour = min(unvisited_neighbours, key=unvisited_neighbours.get)
            return min_neighbour



             