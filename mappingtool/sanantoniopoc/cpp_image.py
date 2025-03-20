import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import os

def fetch_district_graph(district_name):
    """
    Fetch the road network graph for a specific district from OpenStreetMap.

    Args:
        district_name (str): Name of the district to fetch.

    Returns:
        networkx.Graph: Road network graph.
    """
    print(f"Fetching road network for district: {district_name}")
    try:
        district_graph = ox.graph_from_place(district_name, network_type='drive')
        print(f"Successfully fetched road network for {district_name}.")
        return district_graph
    except Exception as e:
        print(f"Error fetching road network for {district_name}: {e}")
        return None

def find_cpp_route_directed(graph):
    """
    Solve the Chinese Postman Problem (CPP) for a directed graph.

    Args:
        graph (networkx.DiGraph): Directed road network graph.

    Returns:
        list: List of edges representing the CPP route.
    """
    print("Solving CPP route on directed graph...")
    try:
        # Check in-degrees and out-degrees
        in_degrees = dict(graph.in_degree())
        out_degrees = dict(graph.out_degree())

        # Calculate imbalance
        imbalance = {node: out_degrees[node] - in_degrees[node] for node in graph.nodes}
        positive_imbalance = {k: v for k, v in imbalance.items() if v > 0}
        negative_imbalance = {k: -v for k, v in imbalance.items() if v < 0}

        # If no imbalance, graph is already Eulerian
        if not positive_imbalance and not negative_imbalance:
            print("Graph is already Eulerian.")
            return list(nx.eulerian_circuit(graph))

        # Check if the graph is strongly connected
        if not nx.is_strongly_connected(graph):
            raise ValueError("Graph is not strongly connected. Cannot solve CPP.")

        # Add virtual edges iteratively
        print("Graph is not Eulerian. Balancing the graph...")
        shortest_paths = dict(nx.all_pairs_dijkstra_path_length(graph))
        while positive_imbalance and negative_imbalance:
            for u, excess in list(positive_imbalance.items()):
                for v, deficit in list(negative_imbalance.items()):
                    if excess > 0 and deficit > 0:
                        # Ensure the nodes are reachable
                        if v not in shortest_paths[u]:
                            print(f"No valid path between {u} and {v}. Skipping.")
                            continue
                        cost = shortest_paths[u][v]
                        print(f"Adding virtual edge from {u} to {v} with cost {cost}.")
                        graph.add_edge(u, v, weight=cost)
                        positive_imbalance[u] -= 1
                        negative_imbalance[v] -= 1

                        # Remove balanced nodes
                        if positive_imbalance[u] == 0:
                            del positive_imbalance[u]
                        if negative_imbalance[v] == 0:
                            del negative_imbalance[v]

        # Verify all imbalances are resolved
        in_degrees = dict(graph.in_degree())
        out_degrees = dict(graph.out_degree())
        imbalance = {node: out_degrees[node] - in_degrees[node] for node in graph.nodes}

        if any(imbalance.values()):
            raise ValueError(f"Graph is still imbalanced after adding virtual edges: {imbalance}")

        # Ensure the graph is Eulerian
        if not nx.is_eulerian(graph):
            raise ValueError("Graph is still not Eulerian after balancing.")

        # Generate Eulerian circuit
        cpp_route = list(nx.eulerian_circuit(graph))
        print("Successfully solved CPP route.")
        return cpp_route
    except Exception as e:
        print(f"Error solving CPP route: {e}")
        return None



def plot_cpp_route(graph, cpp_route, district_name, output_dir):
    """
    Plot the CPP route on the district road network.

    Args:
        graph (networkx.Graph): Road network graph.
        cpp_route (list): List of edges representing the CPP route.
        district_name (str): Name of the district.
        output_dir (str): Directory to save the map.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the road network
    ox.plot_graph(graph, ax=ax, show=False, close=False, node_size=10, edge_color='gray', edge_linewidth=0.5)

    # Highlight the CPP route
    edge_color = 'red'
    edge_width = 2
    for u, v in cpp_route:
        if graph.has_edge(u, v):
            edge = graph[u][v][0]
            x_coords, y_coords = zip(*edge['geometry'].coords)
            ax.plot(x_coords, y_coords, color=edge_color, linewidth=edge_width)

    plt.title(f"CPP Route for {district_name}")
    output_path = os.path.join(output_dir, f"cpp_route_{district_name}.png")
    plt.savefig(output_path)
    print(f"Saved CPP route map for {district_name} to {output_path}")
    plt.close()

def main():
    district_name = "Alamo heights, Texas, USA"  # Name of the district
    output_directory = "cpp_routes"  # Directory to save maps

    # Fetch the road network graph for the district
    graph = fetch_district_graph(district_name)

    if graph is not None:
        # Solve CPP route for directed graphs
        cpp_route = find_cpp_route_directed(graph)

        if cpp_route is not None:
            # Plot and save the CPP route
            plot_cpp_route(graph, cpp_route, district_name, output_directory)
    else:
        print(f"Failed to process district {district_name}.")


if __name__ == "__main__":
    main()
