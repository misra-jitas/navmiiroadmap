import osmnx as ox
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Define the new GeoJSON-like data
geojson_polygon = {
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
line_coords = geojson_polygon['features'][0]['geometry']['coordinates']

# Ensure the first and last coordinates are the same to form a Polygon
if line_coords[0] != line_coords[-1]:
    line_coords.append(line_coords[0])

# Convert to Polygon
polygon = Polygon(line_coords)

# Extract road network using OSMnx
road_network = ox.graph_from_polygon(polygon, network_type="all")

# Plot the road network
fig, ax = ox.plot_graph(
    road_network,
    bgcolor='none',  # Set background to transparent
    show=False,      # Do not display the plot
    close=True       # Close the plot after saving
)

# Save the figure with a transparent background
output_path = "san_antonio_streets_transparent_v3.png"
fig.savefig(output_path, dpi=300, transparent=True)

print(f"Road network visualization saved as '{output_path}'")
