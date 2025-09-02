import geopandas as gpd
import os
import numpy as np
from google.colab import files
import matplotlib.pyplot as plt

def main():
    # Upload the shapefile
    uploaded = files.upload()

    # Get the shapefile name
    shapefile_name = list(uploaded.keys())[0]

    # Path to your shapefile in Colab environment
    shapefile_path = shapefile_name

    # Check if .shx file exists
    if not os.path.exists(shapefile_path.replace(".shp", ".shx")):
        print(".shx file not found. Please ensure that the uploaded shapefile is not corrupted.")
        raise FileNotFoundError(f"The .shx file for {shapefile_name} was not found. Please upload the complete shapefile.")

    # Read the shapefile using geopandas
    try:
        gdf = gpd.read_file(shapefile_path)
    except Exception as e:
        print(f"Error reading the shapefile: {e}")
        raise e

    # Print the GeoDataFrame
    print(gdf)

    # Step 1: Read shapefile and extract coordinate data (Easting and Northing)
    original_data = gdf[['Easting', 'Northing']].dropna().to_numpy()

    # Step 2: Watermarking function
    def watermark_data(data, key, epsilon=1e-5):
        np.random.seed(key)
        noise = np.random.uniform(-epsilon, epsilon, data.shape)
        return data + noise, noise

    # Step 3: Embed watermark
    key = 12345
    watermarked_data, watermark = watermark_data(original_data, key)

    # Step 4: Verify watermark
    def verify_watermark(original, watermarked, key, epsilon=1e-5, tolerance=1e-7):
        regenerated, _ = watermark_data(original, key, epsilon)
        diff = np.abs(regenerated - watermarked)
        return np.all(diff < tolerance), diff

    verified, difference_matrix = verify_watermark(original_data, watermarked_data, key)

    # Step 5: Display results
    print("Original Data Sample:\n", original_data[:5])
    print("\nWatermarked Data Sample:\n", watermarked_data[:5])
    print("\nDifference Matrix Sample:\n", difference_matrix[:5])
    print("\nOwnership Verified:", verified)

    # Visualization
    # Extract Easting and Northing coordinates
    original_easting = original_data[:, 0]
    original_northing = original_data[:, 1]
    watermarked_easting = watermarked_data[:, 0]
    watermarked_northing = watermarked_data[:, 1]

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot original data with circles
    plt.plot(original_easting, original_northing, 'o', label='Original Data', markersize=4)

    # Plot watermarked data with crosses
    plt.plot(watermarked_easting, watermarked_northing, 'x', label='Watermarked Data', markersize=4)

    # Add labels and title
    plt.xlabel('Easting')
    plt.ylabel('Northing')
    plt.title('Original vs. Watermarked Data')
    plt.legend()

    # Display the plot
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()