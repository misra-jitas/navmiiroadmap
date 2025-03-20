import geopandas as gpd
import matplotlib.pyplot as plt
import os
import osmnx as ox

def load_geojson(file_path):
    """
    Load a GeoJSON file.

    Args:
        file_path (str): Path to the GeoJSON file.

    Returns:
        geopandas.GeoDataFrame: Loaded GeoDataFrame.
    """
    try:
        data = gpd.read_file(file_path)
        print(f"Successfully loaded data from {file_path}")
        return data
    except Exception as e:
        print(f"Error loading GeoJSON: {e}")
        return None

def fetch_san_antonio_districts():
    """
    Fetch subdistrict boundaries for San Antonio from OpenStreetMap.

    Returns:
        geopandas.GeoDataFrame: District boundaries.
    """
    print("Fetching subdistrict boundaries for San Antonio from OSM...")
    try:
        # Fetch the geometry of San Antonio
        san_antonio_area = ox.geocode_to_gdf("San Antonio, Texas, USA")
        
        # Fetch all administrative boundaries within the geometry
        san_antonio_districts = ox.features_from_polygon(
            san_antonio_area.geometry[0], tags={"boundary": "administrative"}
        )

        # Filter for admin levels corresponding to subdistricts
        if "admin_level" in san_antonio_districts.columns:
            districts = san_antonio_districts[
                san_antonio_districts["admin_level"].isin(["8", "9", "10"])
            ]
            print(f"Successfully fetched {len(districts)} subdistricts.")
            return districts
        else:
            print("No admin_level data found in OSM response.")
            return gpd.GeoDataFrame()
    except Exception as e:
        print(f"Error fetching subdistricts: {e}")
        return None


def calculate_statistics(district_gdf):
    """
    Calculate basic statistics for a district.

    Args:
        district_gdf (geopandas.GeoDataFrame): GeoDataFrame of the district.

    Returns:
        dict: Dictionary of calculated statistics.
    """
    stats = {
        "Area (sq.km)": district_gdf.to_crs(epsg=3857).area.sum() / 1e6,
        "Bounding Box": district_gdf.total_bounds.tolist(),
        "Centroid": district_gdf.geometry.centroid.iloc[0].coords[0]
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

def plot_district(dca_gdf, district_gdf, district_name, output_dir):
    """
    Plot a single district, highlighting it on the full DCA map.

    Args:
        dca_gdf (geopandas.GeoDataFrame): Full DCA GeoDataFrame.
        district_gdf (geopandas.GeoDataFrame): Single district GeoDataFrame.
        district_name (str): Name of the district.
        output_dir (str): Directory to save the district map.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Plot the full DCA
    fig, ax = plt.subplots(figsize=(10, 10))
    dca_gdf.plot(ax=ax, color='lightgrey', edgecolor='black', alpha=0.5)

    # Highlight the current district
    district_gdf.plot(ax=ax, color='blue', edgecolor='black', alpha=0.7)

    # Add title and labels
    plt.title(f"District: {district_name}")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # Save the figure
    output_path = os.path.join(output_dir, f"district_{district_name}.png")
    plt.savefig(output_path)
    print(f"Saved map for district '{district_name}' to {output_path}")
    plt.close()

def main():
    dca_path = "DCA.geojson"  # Path to the full DCA GeoJSON
    output_directory = "district_maps"  # Directory to save outputs
    stats_output_file = "district_statistics.txt"  # File to save statistics

    # Clear or create the statistics file
    open(stats_output_file, 'w').close()

    # Load the DCA GeoJSON
    dca_data = load_geojson(dca_path)

    # Fetch San Antonio districts from OSM
    districts_data = fetch_san_antonio_districts()

    if dca_data is not None and districts_data is not None:
        districts_data = districts_data.to_crs(dca_data.crs)

        print("Districts found:")
        print(districts_data[["name", "geometry"]])
        print(f"Total districts: {len(districts_data)}")

        for idx, district in districts_data.iterrows():
            district_gdf = gpd.GeoDataFrame([district], crs=districts_data.crs)
            district_name = district.get('name', f'District_{idx}')
            district_name = district_name.replace(' ', '_').replace('/', '_')  # Ensure valid filenames

            # Calculate statistics for the district
            stats = calculate_statistics(district_gdf)
            save_statistics(stats, district_name, stats_output_file)

            # Plot the district
            plot_district(dca_data, district_gdf, district_name, output_directory)
    else:
        print("Failed to load required data.")

if __name__ == "__main__":
    main()
