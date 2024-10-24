#TSP.py
import random
random.seed(42)
def generate_random_route(n_cities):
    route = list(range(1, n_cities))  
    random.shuffle(route)
    return [0]+route  

def compute_distance(city1, city2, distances):
    return distances[city1][city2]

def compute_route_distance(route, distances):
    total_distance = 0
    for i in range(len(route)):
        total_distance += compute_distance(route[i], route[(i+1) % len(route)], distances)
    return total_distance
