import rasterio
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def classify_image(input_image, output_image):
    # Load the input image
    with rasterio.open(input_image) as src:
        image = src.read()
        profile = src.profile

    # Flatten the image to 2D array (pixels x bands)
    n_bands, height, width = image.shape
    image_2d = image.reshape((n_bands, height * width)).T

    # Generate dummy labels (for example purposes)
    labels = np.random.randint(0, 2, size=(height * width))

    # Train a RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(image_2d, labels)

    # Predict the labels
    predicted_labels = clf.predict(image_2d)
    classified_image = predicted_labels.reshape((height, width))

    # Save the classified image
    profile.update(count=1, dtype=rasterio.uint8)
    with rasterio.open(output_image, 'w', **profile) as dst:
        dst.write(classified_image, 1)

    print(f"Classification completed and saved to {output_image}")

# Example usage
def main():
    classify_image("input.tiff", "classified.tiff")

if __name__ == "__main__":
    main()
