import random
import numpy as np
import matplotlib.pyplot as plt

class GeneticAlgorithm:
    def __init__(self, tsp, pop_size=100, num_generations=600, mutation_rate=0.1):
        self.tsp = tsp
        self.pop_size = pop_size
        self.num_generations = num_generations
        self.mutation_rate = mutation_rate

    def create_initial_population(self):
        population = []
        for _ in range(self.pop_size):
            individual = list(np.random.permutation(self.tsp.num_cities))
            individual.append(individual[0])  # Quay lại thành phố đầu tiên
            population.append(individual)
        return population

    def evaluate_population(self, population):
        fitness_scores = []
        for individual in population:
            fitness_scores.append(self.tsp.total_distance(individual))
        return fitness_scores

    def select_parents(self, population, fitness_scores, num_parents):
        parents = np.array(population)[np.argsort(fitness_scores)[:num_parents]]
        return parents.tolist()

    def crossover(self, parent1, parent2):
        size = len(parent1)
        if size < 2:
            raise ValueError("Size of parent must be at least 2 for crossover.")
        start, end = sorted(random.sample(range(1, size - 1), 2))
        child = [None] * size
        child[start:end] = parent1[start:end]
        pointer = 0
        for gene in parent2:
            if gene not in child:
                while child[pointer] is not None:
                    pointer += 1
                child[pointer] = gene
        child[-1] = child[0]
        return child

    def mutate(self, individual):
        for i in range(1, len(individual) - 1):
            if random.random() < self.mutation_rate:
                j = random.randint(1, len(individual) - 2)
                individual[i], individual[j] = individual[j], individual[i]

    def run(self):
        population = self.create_initial_population()
        best_fitness = float('inf')
        best_individual = None

        for generation in range(self.num_generations):
            fitness_scores = self.evaluate_population(population)
            parents = self.select_parents(population, fitness_scores, self.pop_size // 2)

            if len(parents) % 2 != 0:
                parents = parents[:-1]

            next_population = []
            for i in range(0, len(parents), 2):
                parent1, parent2 = parents[i], parents[i + 1]
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                self.mutate(child1)
                self.mutate(child2)
                next_population.extend([child1, child2])

            population = next_population

            # Đánh giá lại fitness của quần thể mới
            fitness_scores = self.evaluate_population(population)
            best_gen_fitness = min(fitness_scores)
            best_gen_individual = population[np.argmin(fitness_scores)]

            # Cập nhật cá thể tốt nhất nếu cần
            if best_gen_fitness < best_fitness:
                best_fitness = best_gen_fitness
                best_individual = best_gen_individual

            # Hiển thị lộ trình và tổng khoảng cách tốt nhất của thế hệ hiện tại
            # print(f"Generation {generation + 1}: Best path {best_gen_individual}, Total distance: {best_gen_fitness:.2f}")

        return best_individual