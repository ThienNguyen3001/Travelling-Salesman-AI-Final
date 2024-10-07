from GA_nhut import GeneticAlgorithm
from Problem import TravellingSalesmanProblem
import matplotlib.pyplot as plt

# Cell 1: Create an instance and print cities and distance matrix
num_cities = 6
max_coordinate = 100

# Prompt user to input coordinates or generate randomly
use_custom_coordinates = input("Do you want to input custom coordinates? (yes/no): ").strip().lower()
if use_custom_coordinates == 'yes':
    cities = TravellingSalesmanProblem.input_coordinates(num_cities)
    tsp = TravellingSalesmanProblem(num_cities, max_coordinate, cities)
else:
    tsp = TravellingSalesmanProblem(num_cities, max_coordinate)

print("Cities:\n", tsp.cities)
print("Distance Matrix:\n", tsp.dist_matrix)
# Cell 2: Visualize the cities
#tsp.visualize_cities()

ga = GeneticAlgorithm(tsp)
best_path = ga.run()

# Trực quan hóa kết quả
plt.figure(figsize=(10, 6))

# Vẽ các thành phố
plt.scatter(tsp.cities[:, 0], tsp.cities[:, 1], c='red')

# Vẽ các cạnh nối tất cả các thành phố với màu xám và nét đứt
for i in range(num_cities):
    for j in range(i + 1, num_cities):
        plt.plot([tsp.cities[i, 0], tsp.cities[j, 0]], 
                 [tsp.cities[i, 1], tsp.cities[j, 1]], 'gray', linestyle='--',linewidth=1)

# Vẽ lộ trình tốt nhất tìm được với màu xanh và nét đậm
for i in range(len(best_path) - 1):
    plt.plot([tsp.cities[best_path[i], 0], tsp.cities[best_path[i+1], 0]], 
             [tsp.cities[best_path[i], 1], tsp.cities[best_path[i+1], 1]], 'b-', linewidth=3)  # Tăng độ dày

# Hiển thị tên thành phố
for i in range(num_cities):
    plt.text(tsp.cities[i, 0], tsp.cities[i, 1], f'City {i+1}', fontsize=12)

plt.title('Travelling Salesman Problem using Genetic Algorithm')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.show()
