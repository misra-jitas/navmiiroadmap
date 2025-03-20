import osmnx as ox
import pandas as pd
from shapely.geometry import Polygon

# Define the second GeoJSON-like data
geojson_polygon_2 = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [
                    [
                        -98.5134915005687,
                        29.396923385394246
                    ],
                    [
                        -98.53514519396661,
                        29.40121277054216
                    ],
                    [
                        -98.54350988375029,
                        29.403785612478174
                    ],
                    [
                        -98.58877155558558,
                        29.408929821773924
                    ],
                    [
                        -98.64183716947917,
                        29.400358010852656
                    ],
                    [
                        -98.65069689055295,
                        29.397786839233476
                    ],
                    [
                        -98.6290987606336,
                        29.352767441932656
                    ],
                    [
                        -98.62030014442146,
                        29.328715892326457
                    ],
                    [
                        -98.60948870929664,
                        29.316686489744114
                    ],
                    [
                        -98.59915735145267,
                        29.323548963700347
                    ],
                    [
                        -98.55286954889355,
                        29.342872676080475
                    ],
                    [
                        -98.52776672703303,
                        29.355742168858768
                    ],
                    [
                        -98.51349117177894,
                        29.378908381569815
                    ],
                    [
                        -98.51250711083122,
                        29.396923315298352
                    ]
                ],
                "type": "LineString"
            }
        }
    ]
}

# Extract the coordinates and ensure the loop is closed
line_coords_2 = geojson_polygon_2['features'][0]['geometry']['coordinates']

# Ensure the first and last coordinates are the same to form a Polygon
if line_coords_2[0] != line_coords_2[-1]:
    line_coords_2.append(line_coords_2[0])

# Convert to Polygon
polygon_2 = Polygon(line_coords_2)

# Extract road network using OSMnx
road_network_2 = ox.graph_from_polygon(polygon_2, network_type="all")

# Calculate total nodes and edges
nodes_2, edges_2 = ox.graph_to_gdfs(road_network_2)

# Calculate the polygon area in square kilometers
polygon_area_km2_2 = polygon_2.area * (111 ** 2)  # Approximate using lat/lon scaling

# Calculate basic road network stats
total_road_length_2 = edges_2['length'].sum()
num_intersections_2 = len(nodes_2)
node_density_2 = num_intersections_2 / polygon_area_km2_2
average_street_segment_length_2 = total_road_length_2 / len(edges_2)

# Flatten the road types for analysis
flattened_road_types_2 = edges_2['highway'].explode() if edges_2['highway'].apply(lambda x: isinstance(x, list)).any() else edges_2['highway']
road_type_counts_2 = flattened_road_types_2.value_counts()

# Prepare a summary
summary_2 = {
    "Total Road Length (meters)": total_road_length_2,
    "Number of Intersections (Nodes)": num_intersections_2,
    "Average Street Segment Length (meters)": average_street_segment_length_2,
    "Node Density (per sq.km)": node_density_2,
    "Polygon Area (sq.km)": polygon_area_km2_2,
    "Road Type Distribution": road_type_counts_2.to_dict()
}

# Save road type data to a CSV
edges_2.to_csv("road_network_stats_polygon_2.csv")

# Display summary in the terminal
print("\n=== Road Network Statistics for Polygon 2 ===")
for key, value in summary_2.items():
    print(f"{key}: {value}")

# Save summary to a CSV
summary_df_2 = pd.DataFrame([summary_2])
summary_df_2.to_csv("summary_stats_polygon_2.csv", index=False)
print("\nSummary saved to 'summary_stats_polygon_2.csv'.")

