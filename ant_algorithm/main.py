from src.graph import Graph
from src.antColonyOptimizer import AntColonyOptimizer
import matplotlib.pyplot as plt


graph = Graph.load_from_file('synthetic.txt', ",")

evaporation_rate = 0.0  # Скорость испарения феромонов
a = 3.0
b = 2.0
max_stagnation = 600
difference = 1.
show = False # Визуализация (не доделана)

aco = AntColonyOptimizer(graph, evaporation_rate, a, b, max_stagnation, difference)
best_tour, best_distance, total_iterations = aco.optimize(show=show)

print("Лучший найденный гамильтонов цикл:", [node.name for node in best_tour])
print("Длина лучшего цикла:", best_distance)
print("Количество итераций:", total_iterations)

# print(aco.all_tours)
x = list(range(len(aco.all_tours)))

plt.plot(x, aco.all_tours, linestyle='-', color='b') 

plt.title('Длина пути на каждой итерации')
plt.xlabel('Итерация')
plt.ylabel('Длина пути')

plt.show()