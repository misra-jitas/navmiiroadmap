import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd

# Define the city
place_name = "San Antonio, Texas, USA"

# Extract road network
G = ox.graph_from_place(place_name, network_type="drive")

# Convert to undirected graph
G_undirected = G.to_undirected()

# Compute the largest connected component
largest_cc = max(nx.connected_components(G_undirected), key=len)
G_largest = G.subgraph(largest_cc).copy()

# Compute centrality measures
degree_centrality = nx.degree_centrality(G_largest)
betweenness_centrality = nx.betweenness_centrality(G_largest, normalized=True, weight="length")

# Convert graph to GeoDataFrames
nodes, edges = ox.graph_to_gdfs(G_largest)

# Add centrality measures
edges["degree_centrality"] = edges.apply(lambda row: degree_centrality.get(row.name[0], 0), axis=1)
edges["betweenness_centrality"] = edges.apply(lambda row: betweenness_centrality.get(row.name[0], 0), axis=1)

# Plot by betweenness centrality
fig, ax = plt.subplots(figsize=(12, 12))
edges.plot(ax=ax, column="betweenness_centrality", cmap="coolwarm", linewidth=0.8, legend=True)
ax.set_title("San Antonio Road Network - Betweenness Centrality", fontsize=14)
plt.show()
