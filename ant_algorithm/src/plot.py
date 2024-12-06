import matplotlib.pyplot as plt
from src.antColonyOptimizer import AntColonyOptimizer

def create_plot(aco: AntColonyOptimizer):
    x = list(range(aco.total_iterations))
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(x, aco.best_all_tours, linestyle='-', color='b') 

    plt.title('Длина лучшего пути на каждой итерации')
    plt.xlabel('Итерация')
    plt.ylabel('Длина пути')

    plt.subplot(1, 2, 2)

    plt.plot(x, aco.all_tours, linestyle='-', color='b') 

    plt.title('Длина пути на каждой итерации')
    plt.xlabel('Итерация')
    plt.ylabel('Длина пути')

    plt.show()