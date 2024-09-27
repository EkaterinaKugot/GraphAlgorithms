from graph import Graph

graph = Graph.load_from_file('data.txt')

start_node = graph.get_node_by_name("1") # Начальное значение
target_node = graph.get_node_by_name("9") # Конечное значение

if start_node and target_node:
    path, distance = graph.dijkstra(start_node, target_node)

    print("Кратчайший путь:", [node.name for node in path])
    print("Расстояние:", distance)
else:
    print("Некорректные исходные данные.")