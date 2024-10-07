import numpy as np
import matplotlib.pyplot as plt
import random
class TravellingSalesmanProblem:
    def __init__(self, num_cities, max_coordinate, cities=None):
        self.num_cities = num_cities
        self.max_coordinate = max_coordinate
        self.cities = cities if cities is not None else self._generate_cities()
        self.dist_matrix = self._calculate_distance_matrix()

    def _generate_cities(self):
        return np.random.randint(0, self.max_coordinate, size=(self.num_cities, 2))

    def _calculate_distance_matrix(self):
        num_cities = self.cities.shape[0]
        dist_matrix = np.zeros((num_cities, num_cities))
        for i in range(num_cities):
            for j in range(num_cities):
                dist_matrix[i, j] = np.linalg.norm(self.cities[i, :2] - self.cities[j, :2])
        return dist_matrix

    def total_distance(self, path):
        return sum(self.dist_matrix[path[i], path[i + 1]] for i in range(len(path) - 1))

    def visualize_cities(self):
        plt.figure(figsize=(10, 6))
        plt.scatter(self.cities[:, 0], self.cities[:, 1], c='red')

        for i in range(self.num_cities):
            plt.text(self.cities[i, 0], self.cities[i, 1], f'City {i+1}', fontsize=12)

        # Nối các thành phố với nhau bằng các đường thẳng
        for i in range(self.num_cities):
            for j in range(i + 1, self.num_cities):
                plt.plot([self.cities[i, 0], self.cities[j, 0]], [self.cities[i, 1], self.cities[j, 1]], 'gray')
        plt.show()

    @staticmethod
    def input_coordinates(num_cities):
        cities = []
        for i in range(num_cities):
            x = int(input(f"Enter x coordinate for city {i+1}: "))
            y = int(input(f"Enter y coordinate for city {i+1}: "))
            cities.append([x, y])
        return np.array(cities)