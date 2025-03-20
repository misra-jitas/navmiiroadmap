import osmnx as ox
import pandas as pd
from shapely.geometry import Polygon

# Define the first GeoJSON-like data
geojson_polygon_1 = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [
                    [
                        -98.47816838139444,
                        29.438280938216778
                    ],
                    [
                        -98.4460661765404,
                        29.43939258308535
                    ],
                    [
                        -98.41602192622206,
                        29.4534777964909
                    ],
                    [
                        -98.40523207436401,
                        29.474387845032254
                    ],
                    [
                        -98.40457386368081,
                        29.454210690840114
                    ],
                    [
                        -98.40307627564411,
                        29.449581379739826
                    ],
                    [
                        -98.39945794246324,
                        29.446061903125425
                    ],
                    [
                        -98.39115738868276,
                        29.4384662735969
                    ],
                    [
                        -98.39030210251434,
                        29.43587225580147
                    ],
                    [
                        -98.41433190359099,
                        29.429014772050593
                    ],
                    [
                        -98.42047065039804,
                        29.42567189366555
                    ],
                    [
                        -98.44135663963314,
                        29.404919956334638
                    ],
                    [
                        -98.44690700428535,
                        29.402342914131594
                    ],
                    [
                        -98.46922950078063,
                        29.401394195963235
                    ],
                    [
                        -98.47858962335076,
                        29.39561999139231
                    ],
                    [
                        -98.48157088379875,
                        29.402858471057
                    ],
                    [
                        -98.48093266834584,
                        29.410283100532
                    ],
                    [
                        -98.48199764113124,
                        29.425307517565088
                    ],
                    [
                        -98.48199768612378,
                        29.428273264305687
                    ],
                    [
                        -98.47923239488009,
                        29.432166737009553
                    ],
                    [
                        -98.47816806170188,
                        29.439207353088634
                    ]
                ],
                "type": "LineString"
            }
        }
    ]
}

# Extract the coordinates and ensure the loop is closed
line_coords_1 = geojson_polygon_1['features'][0]['geometry']['coordinates']

# Ensure the first and last coordinates are the same to form a Polygon
if line_coords_1[0] != line_coords_1[-1]:
    line_coords_1.append(line_coords_1[0])

# Convert to Polygon
polygon_1 = Polygon(line_coords_1)

# Extract road network using OSMnx
road_network_1 = ox.graph_from_polygon(polygon_1, network_type="all")

# Calculate total nodes and edges
nodes, edges = ox.graph_to_gdfs(road_network_1)

# Calculate the polygon area in square kilometers
polygon_area_km2 = polygon_1.area * (111 ** 2)  # Approximate using lat/lon scaling

# Calculate basic road network stats
total_road_length = edges['length'].sum()
num_intersections = len(nodes)
node_density = num_intersections / polygon_area_km2
average_street_segment_length = total_road_length / len(edges)

# Flatten the road types for analysis
flattened_road_types = edges['highway'].explode() if edges['highway'].apply(lambda x: isinstance(x, list)).any() else edges['highway']
road_type_counts = flattened_road_types.value_counts()

# Prepare a summary
summary_1 = {
    "Total Road Length (meters)": total_road_length,
    "Number of Intersections (Nodes)": num_intersections,
    "Average Street Segment Length (meters)": average_street_segment_length,
    "Node Density (per sq.km)": node_density,
    "Polygon Area (sq.km)": polygon_area_km2,
    "Road Type Distribution": road_type_counts.to_dict()
}

# Save road type data to a CSV
edges.to_csv("road_network_stats_polygon_1.csv")

# Display summary in the terminal
print("\n=== Road Network Statistics for Polygon 1 ===")
for key, value in summary_1.items():
    print(f"{key}: {value}")

# Save summary to a CSV
summary_df = pd.DataFrame([summary_1])
summary_df.to_csv("summary_stats_polygon_1.csv", index=False)
print("\nSummary saved to 'summary_stats_polygon_1.csv'.")
