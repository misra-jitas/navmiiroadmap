import geopandas as gpd
import matplotlib.pyplot as plt
import os
import networkx as nx
import osmnx as ox

def fetch_district_from_osm(district_name):
    """
    Fetch the boundary of a specific district from OpenStreetMap.

    Args:
        district_name (str): Name of the district to fetch.

    Returns:
        geopandas.GeoDataFrame: GeoDataFrame of the district boundary.
    """
    print(f"Fetching boundary for district: {district_name}")
    try:
        district_gdf = ox.geocode_to_gdf(district_name)
        print(f"Successfully fetched boundary for {district_name}.")
        return district_gdf
    except Exception as e:
        print(f"Error fetching boundary for {district_name}: {e}")
        return None

def fetch_segments_and_nodes(district_gdf):
    """
    Fetch all road segments and nodes within a district.

    Args:
        district_gdf (geopandas.GeoDataFrame): GeoDataFrame of the district.

    Returns:
        tuple: Graph, GeoDataFrame of edges, GeoDataFrame of nodes.
    """
    print("Fetching road segments and nodes...")
    try:
        district_polygon = district_gdf.geometry.unary_union
        graph = ox.graph_from_polygon(district_polygon, network_type='drive')
        edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
        nodes = ox.graph_to_gdfs(graph, nodes=True, edges=False)
        print("Successfully fetched road network data.")
        return graph, edges, nodes
    except Exception as e:
        print(f"Error fetching road network: {e}")
        return None, None, None

def plot_district_with_segments(district_gdf, edges_gdf, nodes_gdf, district_name, output_dir):
    """
    Plot the district with road segments and nodes.

    Args:
        district_gdf (geopandas.GeoDataFrame): District GeoDataFrame.
        edges_gdf (geopandas.GeoDataFrame): Edges GeoDataFrame.
        nodes_gdf (geopandas.GeoDataFrame): Nodes GeoDataFrame.
        district_name (str): Name of the district.
        output_dir (str): Directory to save the map.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fig, ax = plt.subplots(figsize=(10, 10))
    district_gdf.plot(ax=ax, color='lightgrey', edgecolor='black', alpha=0.5)
    edges_gdf.plot(ax=ax, color='blue', linewidth=0.5, alpha=0.7)
    nodes_gdf.plot(ax=ax, color='red', markersize=5, alpha=0.7)

    plt.title(f"District: {district_name} with Segments and Nodes")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    output_path = os.path.join(output_dir, f"district_{district_name}_segments_nodes.png")
    plt.savefig(output_path)
    print(f"Saved map for district '{district_name}' to {output_path}")
    plt.close()

def calculate_statistics(edges_gdf, nodes_gdf, district_gdf):
    """
    Calculate extended statistics for road segments and nodes.

    Args:
        edges_gdf (geopandas.GeoDataFrame): Edges GeoDataFrame.
        nodes_gdf (geopandas.GeoDataFrame): Nodes GeoDataFrame.
        district_gdf (geopandas.GeoDataFrame): District GeoDataFrame.

    Returns:
        dict: Extended statistics including average segment length, road density, etc.
    """
    edges_gdf_projected = edges_gdf.to_crs(epsg=3857)
    district_gdf_projected = district_gdf.to_crs(epsg=3857)

    total_length = edges_gdf_projected.geometry.length.sum()
    avg_segment_length = total_length / len(edges_gdf_projected) if len(edges_gdf_projected) > 0 else 0
    district_area = district_gdf_projected.geometry.area.sum()  # Total area in square meters
    road_density = total_length / district_area if district_area > 0 else 0
    avg_speed_kmh = 40  # Assuming average speed of 40 km/h
    total_time_seconds = total_length / (avg_speed_kmh * 1000 / 3600)

    stats = {
        "Number of Segments": len(edges_gdf_projected),
        "Number of Nodes": len(nodes_gdf),
        "Total Road Length (meters)": total_length,
        "Average Segment Length (meters)": avg_segment_length,
        "Road Density (meters per square meter)": road_density,
        "Estimated Total Driving Time (hours)": total_time_seconds / 3600,
    }
    return stats

def save_statistics(stats, district_name, output_file):
    """
    Save statistics for a district to a text file.

    Args:
        stats (dict): Statistics dictionary.
        district_name (str): Name of the district.
        output_file (str): Path to the output text file.
    """
    with open(output_file, 'a') as file:
        file.write(f"District: {district_name}\n")
        for key, value in stats.items():
            file.write(f"  {key}: {value}\n")
        file.write("\n")

def save_segment_length_distribution(edges_gdf, district_name, output_dir):
    """
    Save a histogram of segment lengths.

    Args:
        edges_gdf (geopandas.GeoDataFrame): Edges GeoDataFrame.
        district_name (str): Name of the district.
        output_dir (str): Directory to save the histogram.
    """
    edges_gdf_projected = edges_gdf.to_crs(epsg=3857)
    segment_lengths = edges_gdf_projected.geometry.length
    plt.hist(segment_lengths, bins=[0, 50, 200, 500, 1000, 2000], edgecolor='black')
    plt.title("Segment Length Distribution")
    plt.xlabel("Segment Length (meters)")
    plt.ylabel("Frequency")
    plt.grid(True)
    output_path = os.path.join(output_dir, f"{district_name}_segment_length_distribution.png")
    plt.savefig(output_path)
    print(f"Saved segment length distribution histogram to {output_path}")
    plt.close()

def main():
    district_name = "Alamo Heights, Texas, USA"  # Name of the district to fetch
    output_directory = "district_segments_nodes"  # Directory to save maps
    stats_output_file = "district_segments_nodes_statistics.txt"  # File to save statistics

    # Clear or create the statistics file
    open(stats_output_file, 'w').close()

    # Fetch the district boundary from OSM
    district_gdf = fetch_district_from_osm(district_name)

    if district_gdf is not None:
        # Fetch road segments and nodes
        graph, edges_gdf, nodes_gdf = fetch_segments_and_nodes(district_gdf)
        if graph is None or edges_gdf is None or nodes_gdf is None:
            print(f"Skipping district {district_name} due to missing data.")
            return

        # Calculate statistics
        stats = calculate_statistics(edges_gdf, nodes_gdf, district_gdf)
        save_statistics(stats, district_name, stats_output_file)

        # Save segment length distribution
        save_segment_length_distribution(edges_gdf, district_name, output_directory)

        # Plot district with segments and nodes
        plot_district_with_segments(district_gdf, edges_gdf, nodes_gdf, district_name, output_directory)

    else:
        print(f"Failed to fetch data for district {district_name}.")

if __name__ == "__main__":
    main()
