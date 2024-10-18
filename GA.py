import random
import numpy as np
from TSP import generate_random_route, compute_route_distance

#tournament selection
def tournament_selection(population, fitness_scores, tournament_size=3):
    selected_routes = []
    population_size = len(population)
    for _ in range(population_size // 2):  # Chọn một nửa quần thể cho vòng lai tạo
        # Chọn ngẫu nhiên tournament_size cá thể
        tournament_indices = random.sample(range(population_size), tournament_size)
        tournament_participants = [population[i] for i in tournament_indices]
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        # Chọn cá thể có điểm fitness (distance) thấp nhất
        winner_index = tournament_fitness.index(min(tournament_fitness))
        selected_routes.append(tournament_participants[winner_index])

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
    if algorithm == 'tournament':
        return tournament_selection(population, fitness_scores, tournament_size = 3)
    return []
    
def order_crossover(parent1, parent2):
    split_index = random.randint(1, len(parent1) - 1)
    child1_part1 = parent1[:split_index]
    child1_part2 = [city for city in parent2 if city not in child1_part1]
    child1 = child1_part1 + child1_part2
    
    child2_part1 = parent2[:split_index]
    child2_part2 = [city for city in parent1 if city not in child2_part1]
    child2 = child2_part1 + child2_part2

#Single-Point crossover
def single_point_crossover(parent1, parent2):
    # Chọn ngẫu nhiên một điểm cắt (từ vị trí thứ 1 đến vị trí cuối cùng trừ 1)
    crossover_point = random.randint(1, len(parent1) - 1)
    # Tạo đứa con 1: lấy phần đầu từ parent1 và phần còn lại từ parent2
    child1 = parent1[:crossover_point]
    child1 += [city for city in parent2 if city not in child1]
    # Tạo đứa con 2: lấy phần đầu từ parent2 và phần còn lại từ parent1
    child2 = parent2[:crossover_point]
    child2 += [city for city in parent1 if city not in child2]
    return child1, child2

#rank kết hợp với two point có thể giải đến problem4, mutate = 0,05
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
    if algorithm == 'single_point':
        return single_point_crossover(parent1, parent2)
    return [],[]

#Inversion Mutation
def inversion_mutate(route, mutation_rate):
    # Xác suất xảy ra đột biến
    if random.uniform(0, 1) < mutation_rate:
        # Chọn hai vị trí ngẫu nhiên trong tuyến đường
        start, end = sorted(random.sample(range(1, len(route)), 2))  # Đảm bảo chọn hai vị trí khác nhau và bỏ qua city 0
        # Đảo ngược thứ tự các thành phố trong đoạn được chọn
        route[start:end] = reversed(route[start:end])
    return route

#tổ hợp cua nhut co the giai den problem4 với mutate = 0.05
def scramble_mutate(route, mutation_rate):
    if random.random() < mutation_rate:
        # Select two points
        point1 = random.randint(1, len(route) - 2)  # Ensure point1 is valid
        point2 = random.randint(point1 + 1, len(route) - 1)

        # Scramble the segment between point1 and point2
        scrambled_segment = route[point1:point2]
        random.shuffle(scrambled_segment)

        # Create the mutated route
        mutated_route = route[:point1] + scrambled_segment + route[point2:]
        return mutated_route
    return route

def mutate(route, mutation_rate, algorithm='swap'):
    if algorithm == 'swap':
        return swap_mutate(route, mutation_rate)
    if algorithm == 'scramble':
        return scramble_mutate(route,mutation_rate)
    if algorithm == 'inversion':
        return inversion_mutate(route, mutation_rate)
    return []

def fitness(population, distances):
    fitness_scores = []
    for route in population:
        distance = compute_route_distance(route + [route[0]], distances)
        fitness_scores.append(distance)
    return fitness_scores

def genetic_algorithm(n_cities, distances, population_size=100, generations=100, mutation_rate=0.01, 
                      mutation_algorithm='inversion', selection_algorithm='tournament', crossover_algorithm='single_point'):
    # Tạo quần thể ban đầu 
    population = [generate_random_route(n_cities) for _ in range(population_size)]

    for generation in range(generations):
        # Tính điểm fitness cho từng cá thể
        fitness_scores = fitness(population, distances)

        # Chọn những tuyến đường tốt nhất để tái sản xuất (Sử dụng thuật toán tournament selection)
        selected_routes = selection(population, fitness_scores, selection_algorithm)

        # Thực hiện crossover để tạo ra các cá thể con
        offspring = []
        for i in range(population_size // 2):
            parent1, parent2 = random.sample(selected_routes, 2)  # Chọn ngẫu nhiên hai bố mẹ từ các cá thể đã được chọn
            child1, child2 = crossover(parent1, parent2, crossover_algorithm)  # Sử dụng single-point crossover
            offspring.extend([child1, child2])

        # Đột biến các cá thể con
        for i in range(len(offspring)):
            offspring[i] = mutate(offspring[i], mutation_rate, mutation_algorithm)  # Sử dụng inversion mutation

        # Thay thế quần thể cũ bằng quần thể mới
        population = offspring

    # Tìm tuyến đường tốt nhất trong quần thể cuối cùng
    best_route = population[0]
    best_distance = compute_route_distance(best_route, distances)
    for route in population:
        route_distance = compute_route_distance(route, distances)
        if route_distance < best_distance:
            best_route = route
            best_distance = route_distance
    best_route = best_route + [0]  # Đảm bảo rằng tuyến đường quay về điểm bắt đầu (city 0)

    # Trả về kết quả tốt nhất
    solution = {
        'route': best_route,
        'distance': best_distance,
        'fitness': fitness_scores
    }
    return solution
