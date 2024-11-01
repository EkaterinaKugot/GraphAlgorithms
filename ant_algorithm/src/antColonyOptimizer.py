from src.graph import Graph
from src.ant import Ant
import random
import matplotlib.pyplot as plt
import networkx as nx


class AntColonyOptimizer:
    def __init__(
        self,
        graph: Graph,
        evaporation_rate: float,
        a: float,
        b: float,
        max_stagnation: int = 10,
        difference: float = 0.,
        num_ants: int = 1,
    ):
        if not isinstance(graph, Graph) or not isinstance(num_ants, int) or \
            not isinstance(evaporation_rate, float) or not isinstance(a, float) or \
                not isinstance(b, float) or not isinstance(max_stagnation, int) or \
                    not isinstance(difference, float):
                raise TypeError("Неверный тип данных")
        
        self.graph = graph
        self.num_ants = num_ants # Количество муравьев, идущих одновременно
        self.evaporation_rate = evaporation_rate # Скорость испарения феромонов
        self.a = a # a - параметр, контролирующий влияние rij (количество фермонов на ребре)
        self.b = b # b - параметр, контролирующий влияние nij (привлекательность ребра)
        self.best_tour = None # Лучший путь
        self.best_distance = float('inf') # Лучшая дистанция
        self.stagnation_count = 0
        self.max_stagnation = max_stagnation  # Максимальное количество итераций без улучшения
        self.total_iterations = 0
        self.all_tours = []
        self.difference = difference

    # Поиск лучшего пути
    def optimize(self):
        while True:

            for _ in range(self.num_ants):
                ant = Ant(self.graph)
                start_node = random.choice(list(self.graph.nodes.values()))
                ant.visit_node(start_node)

                while len(ant.tour) < len(self.graph.nodes):
                    next_node = ant.choose_next_node(a=self.a, b=self.b)  

                    if next_node is None:  # Если все узлы посещены
                        break

                    ant.visit_node(next_node)
                
                if start_node in ant.current_node.neighbours.keys():
                    ant.visit_node(start_node)

                # Проверяем, не зашел ли муравей в тупик
                if len(ant.tour) == len(self.graph.nodes) + 1 and ant.tour[-1] == start_node: 
                
                    # Обновление лучшего маршрута
                    if ant.total_distance < self.best_distance:
                        if self.best_distance - ant.total_distance <= self.difference:
                            self.stagnation_count += 1
                        self.best_distance = ant.total_distance
                        self.best_tour = ant.tour
                        self.stagnation_count = 0  # Сброс счетчика стагнации
                    else:
                        self.stagnation_count += 1

                    self.all_tours.append(self.best_distance)
                    self.total_iterations += 1

                    # Обновление феромонов на основе маршрутов
                    delta_pheromone = 1 / ant.total_distance if ant.total_distance > 0 else 0
                    for i in range(len(ant.tour) - 1):
                        self.graph.update_pheromone(ant.tour[i], ant.tour[i + 1], delta_pheromone, self.evaporation_rate)
                
            # Проверка условия остановки
            if self.stagnation_count >= self.max_stagnation:
                break

        return self.best_tour, self.best_distance, self.total_iterations