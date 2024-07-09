import rasterio
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import fiona
from rasterio.features import rasterize
from shapely.geometry import shape
import time

def rasterize_polygons(polygons_shapefile, reference_image):
    # Read reference image to get the dimensions and transform
    with rasterio.open(reference_image) as src:
        transform = src.transform
        out_shape = (src.height, src.width)

    # Read the polygons from the shapefile
    with fiona.open(polygons_shapefile, "r") as shapefile:
        shapes = [(shape(feature["geometry"]), int(feature["properties"]["class_id"])) for feature in shapefile]

    # Rasterize the polygons
    rasterized_labels = rasterize(shapes, transform=transform, out_shape=out_shape, fill=0, dtype=np.uint8)

    return rasterized_labels

def supervised_classification(input_image, polygons_shapefile, output_image):
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

    # Rasterize the labeled polygons
    print("Rasterizing polygons...")
    labels = rasterize_polygons(polygons_shapefile, input_image)
    labels_1d = labels.reshape(height * width)

    # Remove pixels with no label
    mask = labels_1d > 0
    image_2d_masked = image_2d[mask]
    labels_1d_masked = labels_1d[mask]

    # Train a RandomForestClassifier
    print("Training the RandomForestClassifier...")
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(image_2d_masked, labels_1d_masked)

    # Predict the labels
    print("Predicting labels...")
    predicted_labels = clf.predict(image_2d)
    classified_image = predicted_labels.reshape((height, width))

    # Save the classified image
    profile.update(count=1, dtype=rasterio.uint8)
    with rasterio.open(output_image, 'w', **profile) as dst:
        dst.write(classified_image, 1)

    # Log completion and duration
    end_time = time.time()
    print(f"Supervised classification completed and saved to {output_image} in {end_time - start_time:.2f} seconds")

# Example usage
def main():
    input_image = "input.tiff"
    polygons_shapefile = "polygons.shp"
    output_image = "classified.tiff"
    supervised_classification(input_image, polygons_shapefile, output_image)

if __name__ == "__main__":
    main()
