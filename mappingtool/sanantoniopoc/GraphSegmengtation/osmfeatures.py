import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

# Define the place
place_name = "San Antonio, Texas, USA"

# Retrieve the road network (driveable roads)
G = ox.graph_from_place(place_name, network_type="drive")

# Convert graph to GeoDataFrame
edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

# Filter for major roads only (highways and primary roads)
major_roads = edges[edges["highway"].isin(["motorway", "primary", "trunk"])]

# Plot the road network with major roads highlighted
fig, ax = plt.subplots(figsize=(12, 12))
edges.plot(ax=ax, color="lightgray", linewidth=0.5, alpha=0.5, label="All Roads")  # Background roads
major_roads.plot(ax=ax, color="red", linewidth=1, label="Major Roads")  # Highlighted major roads

ax.set_title("San Antonio Road Network - Major Highways & Primary Roads", fontsize=14)
ax.legend()

plt.show()

# Display the first few rows of the extracted road network
print(major_roads[["highway", "name", "geometry"]].head())
