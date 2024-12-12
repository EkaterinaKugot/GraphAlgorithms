from src.graph import Graph
from src.ant import Ant
import random


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
        self.best_all_tours = []
        self.all_tours = []
        self.amount_pheromones_best_tour = []
        self.difference = difference
        self.has_cycle = False

    # Поиск лучшего пути
    def optimize(self):
        count_iter = 0
        while True:

            for _ in range(self.num_ants):
                ant = Ant(self.graph)
                start_node = random.choice(list(self.graph.nodes.values()))
                ant.visit_node(start_node)

                while len(ant.tour) < len(self.graph.nodes):
                    next_node = ant.choose_next_node(a=self.a, b=self.b)  

                    if next_node is None:  # Если все узлы посещены
                        break
                    
                    ant.update_amount_pheromones(ant.tour[-1], next_node)
                    ant.visit_node(next_node)
                
                if start_node in ant.current_node.neighbours.keys():
                    ant.update_amount_pheromones(ant.tour[-1], start_node)
                    ant.visit_node(start_node)

                # Проверяем, не зашел ли муравей в тупик
                if len(ant.tour) == len(self.graph.nodes) + 1 and ant.tour[-1] == start_node: 
                    self.has_cycle = True
                    # Обновление лучшего маршрута
                    if ant.total_distance < self.best_distance:
                        self.best_distance = ant.total_distance
                        self.best_tour = ant.tour
                        self.amount_pheromones_best_tour.append(ant.amount_pheromones)
                        if abs(self.best_distance - ant.total_distance) <= self.difference:
                            self.stagnation_count += 1
                        else:
                            self.stagnation_count = 0  # Сброс счетчика стагнации
                    else:
                        tmp_amount_pheromones = 0
                        for idx in range(1, len(self.best_tour)):
                            tmp_amount_pheromones += self.graph.get_pheromone_level(self.best_tour[idx-1], self.best_tour[idx])

                        self.amount_pheromones_best_tour.append(tmp_amount_pheromones)
                        self.stagnation_count += 1

                    self.best_all_tours.append(self.best_distance)
                    self.all_tours.append(ant.total_distance)
                    self.total_iterations += 1

                    # Обновление феромонов на основе маршрутов
                    delta_pheromone = 1 / ant.total_distance if ant.total_distance > 0 else 0
                    for i in range(len(ant.tour) - 1):
                        self.graph.update_pheromone(ant.tour[i], ant.tour[i + 1], delta_pheromone, self.evaporation_rate)
                    
                elif not self.has_cycle:
                    count_iter += 1
                
            # Проверка условия остановки
            if self.stagnation_count >= self.max_stagnation or count_iter >= self.max_stagnation:
                if count_iter >= self.max_stagnation:
                    self.has_cycle = False
                break

        return self.best_tour, self.best_distance, self.total_iterations