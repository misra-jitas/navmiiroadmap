import geopandas as gpd
import matplotlib.pyplot as plt
import os

def load_dca(file_path):
    """
    Load the DCA GeoJSON file.

    Args:
        file_path (str): Path to the GeoJSON file.

    Returns:
        geopandas.GeoDataFrame: Loaded GeoDataFrame.
    """
    try:
        dca_data = gpd.read_file(file_path)
        print(f"Successfully loaded DCA from {file_path}")
        return dca_data
    except Exception as e:
        print(f"Error loading DCA: {e}")
        return None

def calculate_dca_statistics(dca_gdf):
    """
    Calculate basic statistics for the DCA.

    Args:
        dca_gdf (geopandas.GeoDataFrame): DCA GeoDataFrame.

    Returns:
        dict: A dictionary containing DCA statistics.
    """
    if dca_gdf is None or dca_gdf.empty:
        print("No data available for statistics.")
        return None

    # Calculate statistics
    stats = {
        "Bounding Box": dca_gdf.total_bounds.tolist(),
        "Total Area (sq.km)": dca_gdf.to_crs(epsg=3857).area.sum() / 1e6,
        "Number of Polygons": len(dca_gdf),
        "Average Polygon Area (sq.km)": (dca_gdf.to_crs(epsg=3857).area.mean() / 1e6),
        "Largest Polygon Area (sq.km)": (dca_gdf.to_crs(epsg=3857).area.max() / 1e6),
        "Smallest Polygon Area (sq.km)": (dca_gdf.to_crs(epsg=3857).area.min() / 1e6),
        "CRS": dca_gdf.crs.to_string(),
        "Valid Geometries": dca_gdf.is_valid.all()
    }

    return stats

def plot_dca(dca_gdf, output_dir):
    """
    Plot the DCA polygons and save the image.

    Args:
        dca_gdf (geopandas.GeoDataFrame): DCA GeoDataFrame.
        output_dir (str): Directory to save the plot.
    """
    if dca_gdf is not None:
        fig, ax = plt.subplots(figsize=(10, 10))
        dca_gdf.plot(ax=ax, color='blue', alpha=0.5, edgecolor='black')
        plt.title("San Antonio DCA")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        output_path = os.path.join(output_dir, "san_antonio_dca.png")
        plt.savefig(output_path)
        print(f"DCA plot saved to {output_path}")
    else:
        print("No data to plot.")

def main():
    dca_path = "DCA.geojson"  # Path to the uploaded GeoJSON file
    output_directory = "output"  # Directory to save outputs

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Load the DCA GeoJSON
    dca_data = load_dca(dca_path)

    # Calculate and display statistics
    stats = calculate_dca_statistics(dca_data)
    if stats:
        print("DCA Statistics:")
        for key, value in stats.items():
            print(f"- {key}: {value}")

    # Plot the DCA and save it
    plot_dca(dca_data, output_directory)

if __name__ == "__main__":
    main()
