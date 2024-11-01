from src.graph import Graph
from src.antColonyOptimizer import AntColonyOptimizer
import matplotlib.pyplot as plt
import json

# Загрузка параметров из конфигурационного файла
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

filename = config['filename']
separator = config['separator']
graph = Graph.load_from_file(filename, separator)

evaporation_rate = config['evaporation_rate']  # Скорость испарения феромонов
a = config['a']
b = config['b']
max_stagnation = config['max_stagnation']
difference = config['difference']
show = False # Визуализация (не доделана)

aco = AntColonyOptimizer(graph, evaporation_rate, a, b, max_stagnation, difference)
best_tour, best_distance, total_iterations = aco.optimize(show=show)

print("Лучший найденный гамильтонов цикл:", [node.name for node in best_tour])
print("Длина лучшего цикла:", best_distance)
print("Количество итераций:", total_iterations)

x = list(range(len(aco.all_tours)))

plt.plot(x, aco.all_tours, linestyle='-', color='b') 

plt.title('Длина пути на каждой итерации')
plt.xlabel('Итерация')
plt.ylabel('Длина пути')

plt.show()