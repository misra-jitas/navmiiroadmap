import osmnx as ox
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Define the GeoJSON-like data
geojson_polygon = {
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
output_path = "san_antonio_streets_transparent_v2.png"
fig.savefig(output_path, dpi=300, transparent=True)

print(f"Road network visualization saved as '{output_path}'")
