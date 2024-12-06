import matplotlib.pyplot as plt
from src.antColonyOptimizer import AntColonyOptimizer

class Plot:
    def __init__(self, aco: AntColonyOptimizer) -> None:
        self.aco = aco

    def create_all_plot(self):
        plt.figure(figsize=(15, 6))

        self.create_plot_best_tour()
        self.create_plot_len_tour()
        self.create_plot_amount_pheromones()

        plt.show()

    def create_plot_best_tour(self):
        x = list(range(self.aco.total_iterations))
        plt.subplot(1, 3, 1)
        plt.plot(x, self.aco.best_all_tours, linestyle='-', color='b') 

        plt.title('Длина лучшего пути на каждой итерации')
        plt.xlabel('Итерация')
        plt.ylabel('Длина пути')

    def create_plot_len_tour(self):
        x = list(range(self.aco.total_iterations))

        plt.subplot(1, 3, 2)

        plt.plot(x, self.aco.all_tours, linestyle='-', color='b') 

        plt.title('Длина пути на каждой итерации')
        plt.xlabel('Итерация')
        plt.ylabel('Длина пути')

    def create_plot_amount_pheromones(self):
        x = list(range(self.aco.total_iterations))

        plt.subplot(1, 3, 3)

        plt.plot(x, self.aco.amount_pheromones_best_tour, linestyle='-', color='b') 

        plt.title('Кол. феромнов на лучшем пути на каждой итерации')
        plt.xlabel('Итерация')
        plt.ylabel('Кол. феромнов')