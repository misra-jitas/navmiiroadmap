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
    Fetch district boundaries for San Antonio from OpenStreetMap.

    Returns:
        geopandas.GeoDataFrame: District boundaries.
    """
    print("Fetching San Antonio district boundaries from OSM...")
    try:
        san_antonio_districts = ox.features_from_place(
            "San Antonio, Texas, USA", tags={"boundary": "administrative"}
        )
        print("Successfully fetched district boundaries.")
        return san_antonio_districts
    except Exception as e:
        print(f"Error fetching districts: {e}")
        return None

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

    # Load the DCA GeoJSON
    dca_data = load_geojson(dca_path)

    # Fetch San Antonio districts from OSM
    districts_data = fetch_san_antonio_districts()

    if dca_data is not None and districts_data is not None:
        districts_data = districts_data.to_crs(dca_data.crs)

        for idx, district in districts_data.iterrows():
            district_gdf = gpd.GeoDataFrame([district], crs=districts_data.crs)
            district_name = district.get('name', f'District_{idx}')
            district_name = district_name.replace(' ', '_').replace('/', '_')  # Ensure valid filenames
            plot_district(dca_data, district_gdf, district_name, output_directory)
    else:
        print("Failed to load required data.")

if __name__ == "__main__":
    main()
