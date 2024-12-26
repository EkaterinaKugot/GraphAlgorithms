from src.graph import Graph
from src.node import Node
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
num_ants = config['num_ants']
greedy_ants = config['greedy_ants']

aco = AntColonyOptimizer(graph, evaporation_rate, a, b, max_stagnation, difference, num_ants, greedy_ants)
best_tour, best_distance, total_iterations = aco.optimize()

def find_node_by_name(graph:Graph, name: str):
    for node in graph.nodes.values():
        if node.name == name:
            return node
    return None

if not aco.has_cycle:
    print("Гамильтонов цикл не найден!")

    answer = input("Хотите добавить ребра, чтобы получился цикл? (y, n)")
    if answer == "y":
        all_tours, count_new_edge = graph.create_ham_cycle()
        node_list: list[Node] = [item for sublist in all_tours for item in sublist]
        print("Добавлено", count_new_edge, "ребер.")
        
        flag = True
        for i in range(1, len(node_list)):
            if node_list[i] not in node_list[i-1].neighbours.keys():
                print("No")
                flag = False
                break

        if node_list[0] not in node_list[-1].neighbours.keys():   
            flag = False 
            print("No")
        
        if flag:
            print("Гамильтонов цикл есть!")
        # count_new_edge = graph.create_ham_cycle()
        # print(count_new_edge)
        # count_new_edge, count_v = graph.create_cycle()
        # print(count_new_edge, count_v)
        # print(graph.check_has_cycle())
        best_tour, best_distance, total_iterations = aco.optimize(True)


if aco.has_cycle:
    print("Лучший найденный гамильтонов цикл:", [node.name for node in best_tour])
    print("Длина лучшего цикла:", best_distance)
    print("Количество итераций:", total_iterations)

    if greedy_ants == 0:
        plot = Plot(aco, 3)
        plot.create_all_plot()
    