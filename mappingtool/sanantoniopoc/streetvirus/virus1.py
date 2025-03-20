import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
import json

# Define initial bounding box (small 5-block area in Downtown San Antonio)
north, south, east, west = 29.4270, 29.4235, -98.4870, -98.4920

# Step 1: Extract road network for a small subset of Downtown San Antonio
bbox = (north, south, east, west)
G = ox.graph_from_bbox(bbox, network_type="drive")

# Ensure the graph is the largest strongly connected component
G = nx.subgraph(G, max(nx.strongly_connected_components(G), key=len)).copy()

# Step 2: Identify odd-degree nodes (for Eulerization)
odd_nodes = [node for node, degree in G.degree() if degree % 2 == 1]

# Step 3: Compute shortest paths between odd-degree nodes
distances = {}
for node in odd_nodes:
    lengths = nx.single_source_dijkstra_path_length(G, node, weight='length')
    for target in odd_nodes:
        if target in lengths:
            distances[(node, target)] = lengths[target]

# Step 4: Find minimum-weight matching between odd-degree nodes
K_odd = nx.Graph()
K_odd.add_nodes_from(odd_nodes)
for (u, v), w in distances.items():
    K_odd.add_edge(u, v, weight=w)
matching = nx.algorithms.matching.min_weight_matching(K_odd, maxcardinality=True, weight='weight')

# Step 5: Eulerize the Graph by duplicating edges in the shortest paths
augmented_G = G.copy()
for u, v in matching:
    path = nx.shortest_path(G, u, v, weight='length')
    for i in range(len(path) - 1):
        augmented_G.add_edge(path[i], path[i+1], **G.get_edge_data(path[i], path[i+1])[0])

# Step 6: Compute Eulerian circuit on the Eulerized Graph
eulerian_circuit = list(nx.eulerian_circuit(augmented_G))

# Step 7: Convert to GeoJSON for visualization
def route_to_geojson(route_edges, graph):
    """Convert a list of edges to a GeoJSON FeatureCollection."""
    features = []
    for (u, v) in route_edges:
        if 'geometry' in graph[u][v][0]:
            coords = list(graph[u][v][0]['geometry'].coords)
        else:
            coords = [(graph.nodes[u]['x'], graph.nodes[u]['y']), 
                      (graph.nodes[v]['x'], graph.nodes[v]['y'])]
        feature = {
            "type": "Feature",
            "properties": {"u": u, "v": v},
            "geometry": {"type": "LineString", "coordinates": coords}
        }
        features.append(feature)
    return {"type": "FeatureCollection", "features": features}

# Convert Eulerian circuit to GeoJSON
route_geojson = route_to_geojson(eulerian_circuit, augmented_G)

# Save the route as a GeoJSON file
geojson_filename = "/mnt/data/cpp_route_san_antonio.geojson"
with open(geojson_filename, "w") as f:
    json.dump(route_geojson, f)

# Step 8: Plot the Eulerian circuit
fig, ax = plt.subplots(figsize=(8, 8))
ox.plot_graph(augmented_G, ax=ax, node_size=10, edge_linewidth=0.5, show=False)
plt.title("Eulerized Road Network (San Antonio 5-blocks)")
plt.show()

# Return the generated GeoJSON file
geojson_filename
