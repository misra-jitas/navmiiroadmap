
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
        plt.title("City_Council_Districts")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        output_path = os.path.join(output_dir, "City_Council_Districts.png")
        plt.savefig(output_path)
        print(f"DCA plot saved to {output_path}")
    else:
        print("No data to plot.")

def main():
    dca_path = "Missions.geojson"  # Path to the uploaded GeoJSON file
    output_directory = "output"  # Directory to save outputs

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Load the DCA GeoJSON
    dca_data = load_dca(dca_path)

    # Plot the DCA and save it
    plot_dca(dca_data, output_directory)

if __name__ == "__main__":
    main()
