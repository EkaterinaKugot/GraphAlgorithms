import matplotlib.pyplot as plt
from src.antColonyOptimizer import AntColonyOptimizer

class Plot:
    def __init__(self, aco: AntColonyOptimizer, count_plot: int) -> None:
        self.aco = aco
        self.count_plot = count_plot

    def create_all_plot(self):
        plt.figure(figsize=(15, 6))

        self.create_plot_best_tour()
        self.create_plot_len_tour()
        self.create_plot_amount_pheromones()
        # self.create_plot_chance_move_best_tour()

        plt.show()

    def create_plot_best_tour(self):
        x = list(range(self.aco.total_iterations))
        plt.subplot(1, self.count_plot, 1)
        plt.plot(x, self.aco.best_all_tours, linestyle='-', color='b') 

        plt.title('Длина лучшего пути на каждой итерации')
        plt.xlabel('Итерация')
        plt.ylabel('Длина пути')

    def create_plot_len_tour(self):
        x = list(range(self.aco.total_iterations))

        plt.subplot(1, self.count_plot, 2)

        plt.plot(x, self.aco.all_tours, linestyle='-', color='b') 

        plt.title('Длина пути на каждой итерации')
        plt.xlabel('Итерация')
        plt.ylabel('Длина пути')

    def create_plot_amount_pheromones(self):
        x = list(range(self.aco.total_iterations))

        plt.subplot(1, self.count_plot, 3)

        plt.plot(x, self.aco.amount_pheromones_best_tour, linestyle='-', color='b') 

        plt.title('Кол. феромонов на лучшем пути на каждой итерации')
        plt.xlabel('Итерация')
        plt.ylabel('Кол. феромнов')

    def create_plot_chance_move_best_tour(self):
        x = list(range(self.aco.total_iterations))

        plt.subplot(1, self.count_plot, 4)

        plt.plot(x, self.aco.chance_move_best_tour, linestyle='-', color='b') 

        plt.title('Шанс пойти по на лучшему пути на каждой итерации')
        plt.xlabel('Итерация')
        plt.ylabel('Шанс')