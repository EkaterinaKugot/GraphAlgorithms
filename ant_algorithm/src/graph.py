from src.node import Node


class Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.pheromones: dict = {} # словарь с rij - количество феромонов на дуге i, j

    # Получение уровня феромонов между узлами
    def get_pheromone_level(self, begin: Node, end: Node) -> float:
        if not isinstance(begin, Node) or not isinstance(end, Node):
                raise TypeError("Неверный тип данных")
        
        return self.pheromones.get((begin, end), 0.1)  # Уровень феромона по умолчанию 0.1

    # Обновление уровня феромонов между узлами
    def update_pheromone(self, begin: Node, end: Node, delta_pheromone: float, evaporation_rate: float) -> None:
        if not isinstance(begin, Node) or not isinstance(end, Node) or \
            not isinstance(delta_pheromone, float) or not isinstance(evaporation_rate, float):
                raise TypeError("Неверный тип данных")
        
        current_level = self.get_pheromone_level(begin, end)
        new_level = (1 - evaporation_rate) * current_level + delta_pheromone # rij = (1-p)*rij + дельта rij
        self.pheromones[(begin, end)] = new_level
    
    def check_has_cycle(self) -> bool:
        n = len(self.nodes)
        node_list = list(self.nodes.values())
        for i, v in enumerate(node_list):
            for w in node_list[i+1:]:
                if w not in v.neighbours.keys() and v not in w.neighbours.keys():
                    if len(v.neighbours) + len(w.neighbours) >= n:
                        return True
        return False
    
    def create_cycle(self) -> int:
        n = len(self.nodes)    
        count_edge = 0
        count_v = 0
        node_list = list(self.nodes.values())# Сортируем вершины по количеству соседей (по возрастанию)
        node_list.sort(key=lambda node: len(node.neighbours))

        for v in node_list:
            count_v += 1
            for w in node_list:
                if v == w:
                    continue
                if w not in v.neighbours.keys():
                    if len(v.neighbours) + len(w.neighbours) < n:
                        self.add_edge(v, w, 1.0)
                        count_edge += 1
                        if self.check_has_cycle():
                                return count_edge, count_v
                # if v not in w.neighbours.keys():
                #     self.add_edge(w, v, 1.0)
                #     count_edge += 1
                #     if self.check_has_cycle():
                #              return count_edge
            # print(v)
        return count_edge, count_v
    
    def create_ham_cycle(self) -> int:   
        node_list = list(self.nodes.values())
        node_list.sort(key=lambda node: len(node.neighbours), reverse=True)
        node_dict = {node: True for node in node_list}

        all_tours = []
        
        for node, v in node_dict.items(): 
            if not v:
                continue   

            tour = []
            
            def find_tour(node: Node) -> bool:
                node_dict[node] = False
                tour.append(node)

                node_neighbours = list(node.neighbours.keys())
                node_neighbours.sort(key=lambda n: len(n.neighbours), reverse=True)

                for n in node_neighbours:
                    if not node_dict[n]:
                        continue
                    
                    if find_tour(n):
                        return True 
                
                return True

            find_tour(node)

            all_tours.append(tour)

        count_edge = 0

        for i in range(1, len(all_tours)):
            self.add_edge(all_tours[i-1][-1], all_tours[i][0], 1.0)
            count_edge += 1

        self.add_edge(all_tours[-1][-1], all_tours[0][0], 1.0)
        count_edge += 1

        return all_tours, count_edge

    # Получение узла по имени
    def get_node_by_name(self, name: str) -> Node:
        if not isinstance(name, str):
                raise TypeError("Неверный тип данных")

        return self.nodes.get(name, None)

    # Добавление узла
    def add_node(self, node: Node) -> None:
        if not isinstance(node, Node):
                raise TypeError("Неверный тип данных")
        
        if node.name not in self.nodes.keys():
            self.nodes[node.name] = node

    # Удаление узла
    def remove_node(self, node: Node) -> None:
        if not isinstance(node, Node):
                raise TypeError("Неверный тип данных")
        
        if node.name in self.nodes.keys():
            self.nodes.pop(node.name, None)

    # Добавление связи между узлами
    def add_edge(self, begin: Node, end: Node, weight: float = 0.) -> None:
        if not isinstance(begin, Node) or not isinstance(end, Node):
                raise TypeError("Неверный тип данных")
        if not isinstance(weight, float):
                raise TypeError("Неверный тип данных")
        
        if begin in self.nodes.values() and end in self.nodes.values():
            begin.add_neighbour(end, weight)

    # Удаление связи между узлами
    def remove_edge(self, begin: Node, end: Node) -> None:
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
    
    # Загрузка графа из файла
    @staticmethod
    def load_from_file(file_path: str, split: str = None) -> 'Graph':
        if not isinstance(file_path, str) :
                raise TypeError("Неверный тип данных")
        
        graph = Graph()

        with open(file_path, 'r') as file:
            next(file)
            for line in file:
                if split is not None and split != "":
                    source, target, weight = line.strip().split(split)
                else:
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