import osmnx as ox
import pandas as pd
from shapely.geometry import Polygon

# Define the polygons
polygon_1_coords = [
    [-98.47816838139444, 29.438280938216778],
    [-98.4460661765404, 29.43939258308535],
    [-98.41602192622206, 29.4534777964909],
    [-98.40523207436401, 29.474387845032254],
    [-98.40457386368081, 29.454210690840114],
    [-98.40307627564411, 29.449581379739826],
    [-98.39945794246324, 29.446061903125425],
    [-98.39115738868276, 29.4384662735969],
    [-98.39030210251434, 29.43587225580147],
    [-98.41433190359099, 29.429014772050593],
    [-98.42047065039804, 29.42567189366555],
    [-98.44135663963314, 29.404919956334638],
    [-98.44690700428535, 29.402342914131594],
    [-98.46922950078063, 29.401394195963235],
    [-98.47858962335076, 29.39561999139231],
    [-98.48157088379875, 29.402858471057],
    [-98.48093266834584, 29.410283100532],
    [-98.48199764113124, 29.425307517565088],
    [-98.48199768612378, 29.428273264305687],
    [-98.47923239488009, 29.432166737009553],
    [-98.47816806170188, 29.439207353088634],
    [-98.47816838139444, 29.438280938216778]  # Closed loop
]

polygon_2_coords = [
    [-98.5134915005687, 29.396923385394246],
    [-98.53514519396661, 29.40121277054216],
    [-98.54350988375029, 29.403785612478174],
    [-98.58877155558558, 29.408929821773924],
    [-98.64183716947917, 29.400358010852656],
    [-98.65069689055295, 29.397786839233476],
    [-98.6290987606336, 29.352767441932656],
    [-98.62030014442146, 29.328715892326457],
    [-98.60948870929664, 29.316686489744114],
    [-98.59915735145267, 29.323548963700347],
    [-98.55286954889355, 29.342872676080475],
    [-98.52776672703303, 29.355742168858768],
    [-98.51349117177894, 29.378908381569815],
    [-98.51250711083122, 29.396923315298352],
    [-98.5134915005687, 29.396923385394246]  # Closed loop
]

polygon_3_coords = [
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
    [-98.51156672374776, 29.397516283983535]  # Closed loop
]

# Convert to polygons and extract road networks
polygon_1 = Polygon(polygon_1_coords)
polygon_2 = Polygon(polygon_2_coords)
polygon_3 = Polygon(polygon_3_coords)

road_network_1 = ox.graph_from_polygon(polygon_1, network_type="all")
road_network_2 = ox.graph_from_polygon(polygon_2, network_type="all")
road_network_3 = ox.graph_from_polygon(polygon_3, network_type="all")

nodes_1, edges_1 = ox.graph_to_gdfs(road_network_1)
nodes_2, edges_2 = ox.graph_to_gdfs(road_network_2)
nodes_3, edges_3 = ox.graph_to_gdfs(road_network_3)

# Function to extract and save all road segments for a polygon, including street names
def extract_road_segments_with_names(graph, edges, output_filename):
    # Add 'u', 'v', and 'key' columns from the graph's edges
    edges = edges.copy()  # Ensure the GeoDataFrame is writable
    edges['u'] = edges.index.get_level_values('u')
    edges['v'] = edges.index.get_level_values('v')
    edges['key'] = edges.index.get_level_values('key')

    # Include 'name' column if available, otherwise fill with 'Unnamed'
    edges['name'] = edges['name'].fillna('Unnamed') if 'name' in edges.columns else 'Unnamed'

    # Create a DataFrame with road segment details
    road_segments = edges[['u', 'v', 'key', 'length', 'highway', 'name']]
    road_segments.to_csv(output_filename, index=False)
    print(f"Road segments (with names) extracted and saved as '{output_filename}'")

# Extract and save road segments with names for each polygon
extract_road_segments_with_names(road_network_1, edges_1, "road_segments_with_names_polygon_1.csv")
extract_road_segments_with_names(road_network_2, edges_2, "road_segments_with_names_polygon_2.csv")
extract_road_segments_with_names(road_network_3, edges_3, "road_segments_with_names_polygon_3.csv")
