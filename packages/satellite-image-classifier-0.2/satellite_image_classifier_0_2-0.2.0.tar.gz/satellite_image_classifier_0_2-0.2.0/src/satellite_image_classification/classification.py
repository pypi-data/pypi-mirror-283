import rasterio
import numpy as np
from sklearn.cluster import KMeans
import time

def unsupervised_classification(input_image, output_image, n_clusters=5):
    # Start timing
    start_time = time.time()

    # Load the input image
    with rasterio.open(input_image) as src:
        image = src.read()
        profile = src.profile

    # Log image dimensions
    n_bands, height, width = image.shape
    print(f"Image dimensions: {n_bands} bands, {height} height, {width} width")

    # Flatten the image to 2D array (pixels x bands)
    image_2d = image.reshape((n_bands, height * width)).T

    # Perform K-means clustering
    print(f"Performing K-means clustering with {n_clusters} clusters...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clustered = kmeans.fit_predict(image_2d)
    
    # Reshape clustered data back to the original image dimensions
    classified_image = clustered.reshape((height, width))

    # Save the classified image
    profile.update(count=1, dtype=rasterio.uint8)
    with rasterio.open(output_image, 'w', **profile) as dst:
        dst.write(classified_image.astype(rasterio.uint8), 1)

    # Log completion and duration
    end_time = time.time()
    print(f"Unsupervised classification completed and saved to {output_image} in {end_time - start_time:.2f} seconds")

# Example usage
def main():
    unsupervised_classification("input.tiff", "classified.tiff", n_clusters=5)

if __name__ == "__main__":
    main()
