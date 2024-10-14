from src.graph import Graph
from src.antColonyOptimizer import AntColonyOptimizer


graph = Graph.load_from_file('data.txt')

num_ants = 1 # Количество муравьев идущих одновременно
evaporation_rate = 0.5  # Скорость испарения феромонов
a = 1.0
b = 2.0
max_stagnation = 10
show = False # Визуализация (не доделана)

aco = AntColonyOptimizer(graph, num_ants, evaporation_rate, a, b, max_stagnation)
best_tour, best_distance, total_iterations = aco.optimize(show=show )

print("Лучший найденный гамильтонов цикл:", [node.name for node in best_tour])
print("Длина лучшего цикла:", best_distance)
print("Количество итераций:", total_iterations)