# run.py

from GA import genetic_algorithm

def main():
    # Example distance matrix (symmetric matrix)
    distances = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]
    n_cities = len(distances)

    # Run the genetic algorithm to solve TSP
    solution = genetic_algorithm(n_cities, distances, population_size=50, generations=100, mutation_rate=0.1)

    # Print the result
    print(f"Best route: {solution['route']}")
    print(f"Shortest distance: {solution['distance']}")

if __name__ == "__main__":
    main()
