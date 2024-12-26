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
        greedy_ants: int = 0
    ):
        if not isinstance(graph, Graph) or not isinstance(num_ants, int) or \
            not isinstance(evaporation_rate, float) or not isinstance(a, float) or \
                not isinstance(b, float) or not isinstance(max_stagnation, int) or \
                    not isinstance(difference, float) or not isinstance(greedy_ants, int):
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
        # self.chance_move_best_tour = []
        self.has_cycle = True

        if greedy_ants > num_ants:
            raise ValueError("greedy_ants не может быть больше num_ants")
        
        self.greedy_ants = greedy_ants

    # Поиск лучшего пути
    def optimize(self, second = False):
        if not second and not self.graph.check_has_cycle():
            self.has_cycle = False
            return self.best_tour, self.best_distance, self.total_iterations

        start_greedy_ant = self.num_ants - self.greedy_ants
        while True:
            all_ant: list[Ant] = []
            for i in range(self.num_ants):
                if i >= start_greedy_ant:
                    ant = Ant(self.graph, True)
                else:
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

                has_new_best_dist = False
                # Проверяем, не зашел ли муравей в тупик
                if len(ant.tour) == len(self.graph.nodes) + 1 and ant.tour[-1] == start_node: 
                    # Обновление лучшего маршрута
                    if ant.total_distance < self.best_distance and not ant.greedy:
                        has_new_best_dist = True
                        self.best_distance = ant.total_distance
                        self.best_tour = ant.tour
                        if self.best_tour is None:
                            print(ant.greedy)
                            print(ant)
                            print(ant.tour)
                        self.amount_pheromones_best_tour.append(ant.amount_pheromones)
                    else:
                        tmp_amount_pheromones = 0
                        if self.best_tour is None:
                            self.amount_pheromones_best_tour.append(ant.amount_pheromones)
                        else:
                            for idx in range(1, len(self.best_tour)):
                                tmp_amount_pheromones += self.graph.get_pheromone_level(self.best_tour[idx-1], self.best_tour[idx])

                            self.amount_pheromones_best_tour.append(tmp_amount_pheromones)
                    
                    all_ant.append(ant)

                    # tmp_chance_move = 1
                    # for idx in range(1, len(self.best_tour)):
                    #     pheromone_level = self.graph.get_pheromone_level(self.best_tour[idx-1], self.best_tour[idx])
                    #     distance = self.best_tour[idx-1].neighbours[self.best_tour[idx]]

                    #     if distance == 0:
                    #         attractiveness = 1 + 0.000001
                    #     else:
                    #         attractiveness = 1 / distance
                    #     probability = (pheromone_level ** self.a) * (attractiveness ** self.b)
                    #     tmp_chance_move *= probability
                    # self.chance_move_best_tour.append(tmp_chance_move)

                    self.best_all_tours.append(self.best_distance)
                    self.all_tours.append(ant.total_distance)
                    self.total_iterations += 1

            # Обновление счетчика стагнации
            if not has_new_best_dist and len(all_ant) == 0: # все зашли в тупик
                pass
            elif not has_new_best_dist: 
                self.stagnation_count += 1
            else: 
                self.stagnation_count = 0

            # Обновление феромонов на основе маршрутов
            for ant in all_ant:

                delta_pheromone = 1 / ant.total_distance if ant.total_distance > 0 else 0
                for i in range(len(ant.tour) - 1):
                    self.graph.update_pheromone(ant.tour[i], ant.tour[i + 1], delta_pheromone, self.evaporation_rate)
                
            # Проверка условия остановки
            if self.stagnation_count >= self.max_stagnation:
                break
        if self.best_tour is None:
            self.best_distance = ant.total_distance
            self.best_tour = ant.tour
        return self.best_tour, self.best_distance, self.total_iterations