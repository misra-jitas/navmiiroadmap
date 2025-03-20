import osmnx as ox
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Define GeoJSON-like coordinates for the LineString
line_coords = [
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
    [-98.51199125715345, 29.399743541102637],
    [-98.51156672374776, 29.397516283983535]  # Close the loop
]

# Convert LineString to Polygon
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
output_path = "san_antonio_streets_transparent.png"
fig.savefig(output_path, dpi=300, transparent=True)

print(f"Road network visualization saved as '{output_path}'")
