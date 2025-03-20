import osmnx as ox
import pandas as pd
from shapely.geometry import Polygon

# Define the third GeoJSON-like data (update coordinates if different from the initial polygons)
geojson_polygon_3 = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "coordinates": [
                    # Replace with actual coordinates for Polygon 3
                    [-98.51156672374776, 29.397516283983535],
                    [-98.5122040219124, 29.40271087313471],
                    [-98.50624365557152, 29.413280928114915],
                    [-98.50241105596393, 29.418288481381026],
                    [-98.49900320389264, 29.43386226533613],
                    [-98.48474390933717, 29.441275702290568],
                    [-98.47793519023199, 29.439607945206674],
                    [-98.47772373946428, 29.43516165434444],
                    [-98.48219046553648, 29.428488529198148],
                    [-98.4798488622796, 29.41328382761509],
                    [-98.48091235829374, 29.404560475136464],
                    [-98.47835681360459, 29.395465497165745],
                    [-98.4824022741413, 29.394161196450057],
                    [-98.5009282429177, 29.396390274648297],
                    [-98.51177959950138, 29.39695988798195],
                    [-98.51199125715345, 29.399743541102637]
                ],
                "type": "LineString"
            }
        }
    ]
}

# Extract the coordinates and ensure the loop is closed
line_coords_3 = geojson_polygon_3['features'][0]['geometry']['coordinates']

# Ensure the first and last coordinates are the same to form a Polygon
if line_coords_3[0] != line_coords_3[-1]:
    line_coords_3.append(line_coords_3[0])

# Convert to Polygon
polygon_3 = Polygon(line_coords_3)

# Extract road network using OSMnx
road_network_3 = ox.graph_from_polygon(polygon_3, network_type="all")

# Calculate total nodes and edges
nodes_3, edges_3 = ox.graph_to_gdfs(road_network_3)

# Calculate the polygon area in square kilometers
polygon_area_km2_3 = polygon_3.area * (111 ** 2)  # Approximate using lat/lon scaling

# Calculate basic road network stats
total_road_length_3 = edges_3['length'].sum()
num_intersections_3 = len(nodes_3)
node_density_3 = num_intersections_3 / polygon_area_km2_3
average_street_segment_length_3 = total_road_length_3 / len(edges_3)

# Flatten the road types for analysis
flattened_road_types_3 = edges_3['highway'].explode() if edges_3['highway'].apply(lambda x: isinstance(x, list)).any() else edges_3['highway']
road_type_counts_3 = flattened_road_types_3.value_counts()

# Prepare a summary
summary_3 = {
    "Total Road Length (meters)": total_road_length_3,
    "Number of Intersections (Nodes)": num_intersections_3,
    "Average Street Segment Length (meters)": average_street_segment_length_3,
    "Node Density (per sq.km)": node_density_3,
    "Polygon Area (sq.km)": polygon_area_km2_3,
    "Road Type Distribution": road_type_counts_3.to_dict()
}

# Save road type data to a CSV
edges_3.to_csv("road_network_stats_polygon_3.csv")

# Display summary in the terminal
print("\n=== Road Network Statistics for Polygon 3 ===")
for key, value in summary_3.items():
    print(f"{key}: {value}")

# Save summary to a CSV
summary_df_3 = pd.DataFrame([summary_3])
summary_df_3.to_csv("summary_stats_polygon_3.csv", index=False)
print("\nSummary saved to 'summary_stats_polygon_3.csv'.")
