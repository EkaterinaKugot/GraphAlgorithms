from src.graph import Graph
from src.antColonyOptimizer import AntColonyOptimizer
from src.plot import *
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

aco = AntColonyOptimizer(graph, evaporation_rate, a, b, max_stagnation, difference)
best_tour, best_distance, total_iterations = aco.optimize()

if not aco.has_cycle:
    print("Цикл не найден!")
else:
    print("Лучший найденный гамильтонов цикл:", [node.name for node in best_tour])
    print("Длина лучшего цикла:", best_distance)
    print("Количество итераций:", total_iterations)

    plot = Plot(aco)
    plot.create_all_plot()
    