import networkx as nx
import matplotlib.pyplot as plt
from GA import genetic_algorithm

def main():
    distances = [
        [0, 85, 26, 81],
        [85, 0, 77, 97],
        [26, 77, 0, 26],
        [81, 97, 26, 0]
    ]
    n_cities = len(distances)
    solution = genetic_algorithm(n_cities, distances, population_size=100, generations=10, mutation_rate=0.1)
    
    # Print the route and distance
    print(f"Best route: {solution['route']}")
    print(f"Shortest distance: {solution['distance']}")
    
    # Create a graph
    G = nx.Graph()
    for i in range(n_cities):
        G.add_node(i)
        for j in range(i + 1, n_cities):
            G.add_edge(i, j, weight=distances[i][j])

    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Highlight the best route
    route_edges = [(solution['route'][i], solution['route'][i + 1]) for i in range(len(solution['route']) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='r', width=2)

    plt.show()
if __name__ == "__main__":
    main()