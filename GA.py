from TSPProblem import generate_random_route, compute_route_distance
import random
def selection(population, fitness_scores):
    selected_routes = []
    population_size = len(population)
    for i in range(population_size // 2):
        max_fitness_index = fitness_scores.index(min(fitness_scores))  # Minimize distance
        selected_routes.append(population[max_fitness_index])
        fitness_scores[max_fitness_index] = float('inf')  # Mark as selected
    return selected_routes

def crossover(parent1, parent2):
    split_index = random.randint(1, len(parent1) - 2)
    child1_part1 = parent1[:split_index]
    child1_part2 = [city for city in parent2 if city not in child1_part1]
    child1 = child1_part1 + child1_part2
    
    child2_part1 = parent2[:split_index]
    child2_part2 = [city for city in parent1 if city not in child2_part1]
    child2 = child2_part1 + child2_part2

    return child1, child2

def mutate(route, mutation_rate):
    for i in range(len(route)):
        if random.uniform(0, 1) < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]  # Swap mutation
    return route

def genetic_algorithm(n_cities, distances, population_size=100, generations=100, mutation_rate=0.1):
    # Create initial population
    population = [generate_random_route(n_cities) for _ in range(population_size)]

    for generation in range(generations):
        # Calculate fitness of each route (minimize distance)
        fitness_scores = [compute_route_distance(route, distances) for route in population]

        # Select the best routes for reproduction
        selected_routes = selection(population, fitness_scores)

        # Crossover to create offspring
        offspring = []
        for i in range(population_size // 2):
            parent1 = selected_routes[random.randint(0, len(selected_routes) - 1)]
            parent2 = selected_routes[random.randint(0, len(selected_routes) - 1)]
            child1, child2 = crossover(parent1, parent2)
            offspring.extend([child1, child2])

        # Mutate the offspring
        for i in range(len(offspring)):
            offspring[i] = mutate(offspring[i], mutation_rate)

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

    # Return the best solution
    solution = {
        'route': best_route,
        'distance': best_distance
    }
    return solution