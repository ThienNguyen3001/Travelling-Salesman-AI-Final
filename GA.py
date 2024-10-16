import random
import numpy as np
from TSP import generate_random_route, compute_route_distance

def elitism_selection(population, fitness_scores):
    selected_routes = []
    population_size = len(population)
    for i in range(population_size // 2):
        max_fitness_index = fitness_scores.index(min(fitness_scores))  # Minimize distance
        selected_routes.append(population[max_fitness_index])
        fitness_scores[max_fitness_index] = 0  # Mark as selected
    return selected_routes

#voi mutate = 0,5 sẽ cho ra đáp án đến problem3, còn lại thì chỉ gần đúng
def rank_selection(population, fitness_scores):
    sorted_population = [ind for _, ind in sorted(zip(fitness_scores, population))] #sort with fitness
    ranks = np.arange(1, len(population) + 1) #add rank

    probabilities = 1 / ranks
    probabilities /= probabilities.sum()    
    cumulative_probabilities = np.cumsum(probabilities) #mảng cộng dồn

    selected_individuals = []
    population_size = len(population)
    for i in range(population_size // 2):
        r = np.random.rand()  # Tạo số ngẫu nhiên giữa 0 và 1
        for i, cum_prob in enumerate(cumulative_probabilities):
            if r <= cum_prob:
                selected_individuals.append(sorted_population[i])
                break
    return selected_individuals

def selection (population, fitness_scores,algorithm = 'elitism'):
    if algorithm == 'elitism':
        return elitism_selection(population, fitness_scores)
    if algorithm == 'rank':
        return rank_selection(population, fitness_scores)
    return []
    
def order_crossover(parent1, parent2):
    split_index = random.randint(1, len(parent1) - 1)
    child1_part1 = parent1[:split_index]
    child1_part2 = [city for city in parent2 if city not in child1_part1]
    child1 = child1_part1 + child1_part2
    
    child2_part1 = parent2[:split_index]
    child2_part2 = [city for city in parent1 if city not in child2_part1]
    child2 = child2_part1 + child2_part2

    return child1, child2

#rank kết hợp với two point có thể giải đến problem4
def two_point_crossover(parent1, parent2):
    # Select two random points
    point1 = random.randint(1, len(parent1) - 1)
    point2 = random.randint(1, len(parent1) - 1)

    # swap if point 1>point 2
    if point1 > point2:
        point1, point2 = point2, point1

    # Crossover for child1
    child1_part1 = parent1[:point1]
    child1_middle = [city for city in parent2[point1:point2] if city not in child1_part1]
    child1_part3 = [city for city in parent1[point2:] if city not in child1_part1 + child1_middle]
    
    # Fill missing cities from parent2
    missing_cities1 = [city for city in parent2 if city not in child1_part1 + child1_middle + child1_part3]
    child1 = child1_part1 + child1_middle + child1_part3 + missing_cities1

    # Crossover for child2 (similar to child1)
    child2_part1 = parent2[:point1]
    child2_middle = [city for city in parent1[point1:point2] if city not in child2_part1]
    child2_part3 = [city for city in parent2[point2:] if city not in child2_part1 + child2_middle]
    
    # Fill missing cities from parent1
    missing_cities2 = [city for city in parent1 if city not in child2_part1 + child2_middle + child2_part3]
    child2 = child2_part1 + child2_middle + child2_part3 + missing_cities2

    return child1, child2

def crossover(parent1, parent2, algorithm='order'):
    if algorithm == 'order':
        return order_crossover(parent1, parent2)
    if algorithm == 'two_point':
        return two_point_crossover(parent1,parent2)
    return [],[]

def swap_mutate(route, mutation_rate):
    # Ensure that city 0 stays fixed at the start
    for i in range(1,len(route)):  
        if random.uniform(0, 1) < mutation_rate:
            j = random.randint(1, len(route) - 1)  # Swap within non-starting cities
            route[i], route[j] = route[j], route[i]  # Swap mutation
    return route

def mutate(route, mutation_rate, algorithm='swap'):
    if algorithm == 'swap':
        return swap_mutate(route, mutation_rate)
    else:
        return []

def fitness(population, distances):
    fitness_scores = []
    for route in population:
        distance = compute_route_distance(route + [route[0]], distances)
        fitness_scores.append(distance)
    return fitness_scores

def genetic_algorithm(n_cities, distances, population_size=100, generations=100, mutation_rate=0.01, 
                      mutation_algorithm='swap', selection_algorithm='elitism', crossover_algorithm='order'):
    # Create initial population 
    population = [generate_random_route(n_cities) for _ in range(population_size)]

    for generation in range(generations):
        fitness_scores = fitness(population, distances)

        # Select the best routes for reproduction
        selected_routes = selection(population, fitness_scores, selection_algorithm)

        # Crossover to create offspring
        offspring = []
        for i in range(population_size // 2):
            parent1, parent2 = random.sample(selected_routes, 2)
            child1, child2 = crossover(parent1, parent2, crossover_algorithm)
            offspring.extend([child1, child2])

        # Mutate the offspring
        for i in range(len(offspring)):
            offspring[i] = mutate(offspring[i], mutation_rate, mutation_algorithm)

        # Replace the old population with the new offspring
        population = offspring

    # Find the best route
    best_route = population[0]
    best_distance = compute_route_distance(best_route, distances)
    for route in population:
        route_distance = compute_route_distance(route, distances)
        if route_distance < best_distance:
            best_route = route
            best_distance = route_distance
    best_route = best_route + [0] 
    # Return the best solution
    solution = {
        'route': best_route,
        'distance': best_distance,
        'fitness': fitness_scores
    }
    return solution