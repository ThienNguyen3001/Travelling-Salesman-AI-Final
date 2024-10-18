import networkx as nx
import matplotlib.pyplot as plt
from GA import genetic_algorithm

def main():
    distances = [
        [0, 141, 134, 152, 173, 289, 326, 329, 285, 401, 388, 366, 343, 305, 276],
        [141, 0, 152, 150, 153, 312, 354, 313, 249, 324, 300, 272, 247, 201, 176],
        [134, 152, 0, 24, 48, 168, 210, 197, 153, 280, 272, 257, 237, 210, 181],
        [152, 150, 24, 0, 24, 163, 206, 182, 133, 257, 248, 233, 214, 187, 158],
        [173, 153, 48, 24, 0, 160, 203, 167, 114, 234, 225, 210, 190, 165, 137],
        [289, 312, 168, 163, 160, 0, 43, 90, 124, 250, 264, 270, 264, 267, 249],
        [326, 354, 210, 206, 203, 43, 0, 108, 157, 271, 290, 299, 295, 303, 287],
        [329, 313, 197, 182, 167, 90, 108, 0, 70, 164, 183, 195, 194, 210, 201],
        [285, 249, 153, 133, 114, 124, 157, 70, 0, 141, 147, 148, 140, 147, 134],
        [401, 324, 280, 257, 234, 250, 271, 164, 141, 0, 36, 67, 88, 134, 150],
        [388, 300, 272, 248, 225, 264, 290, 183, 147, 36, 0, 33, 57, 104, 124],
        [366, 272, 257, 233, 210, 270, 299, 195, 148, 67, 33, 0, 26, 73, 96],
        [343, 247, 237, 214, 190, 264, 295, 194, 140, 88, 57, 26, 0, 48, 71],
        [305, 201, 210, 187, 165, 267, 303, 210, 147, 134, 104, 73, 48, 0, 30],
        [276, 176, 181, 158, 137, 249, 287, 201, 134, 150, 124, 96, 71, 30, 0]
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