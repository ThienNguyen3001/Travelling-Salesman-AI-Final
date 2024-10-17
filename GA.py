import random
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

def selection(population, fitness_scores, algorithm='tournament', tournament_size=3):
    if algorithm == 'tournament':
        return tournament_selection(population, fitness_scores, tournament_size)
    else:
        return []

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

def crossover(parent1, parent2, algorithm='single_point'):
    if algorithm == 'single_point':
        return single_point_crossover(parent1, parent2)
    else:
        return [], []

#Inversion Mutation
def inversion_mutate(route, mutation_rate):
    # Xác suất xảy ra đột biến
    if random.uniform(0, 1) < mutation_rate:
        # Chọn hai vị trí ngẫu nhiên trong tuyến đường
        start, end = sorted(random.sample(range(1, len(route)), 2))  # Đảm bảo chọn hai vị trí khác nhau và bỏ qua city 0
        # Đảo ngược thứ tự các thành phố trong đoạn được chọn
        route[start:end] = reversed(route[start:end])
    return route

def mutate(route, mutation_rate, algorithm='inversion'):
    if algorithm == 'inversion':
        return inversion_mutate(route, mutation_rate)
    else:
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
