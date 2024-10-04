# import cv2
# import numpy as np
# import json
# import rasterio 
# from osgeo import gdal, osr
# from matplotlib import pyplot as plt

# # Load the reprojected GeoTIFF image
# file_path = r'C:\Users\91844\Desktop\6Simplex\New folder\new_version_for_extraction\reprojected_geotiff_4326.tif'
# image = cv2.imread(file_path)

# if image is None:
#     print(f"Failed to load image at {file_path}")
#     exit(1)
# else:
#     print("Image loaded successfully, dimensions:", image.shape)

# # Get image dimensions
# height, width, _ = image.shape

# # Open the dataset with rasterio to get transformation info
# try:
#     with rasterio.open(file_path) as src:
#         geo_transform = src.transform
#         print("Raster data loaded successfully")
#         print("Width:", src.width, "Height:", src.height)
#         print("Geo Transform:", geo_transform)

#         # Define source spatial reference system (SRS) from dataset projection
#         source_srs = osr.SpatialReference()
#         source_srs.ImportFromWkt(src.crs.to_wkt())  # Ensure correct projection info is used
# except Exception as e:
#     print("Error loading raster data:", e)
#     exit(1)

# # Define the color ranges for blue polygons
# lowerColor1 = np.array([83, 195, 189]) - 10
# upperColor1 = np.array([83, 195, 189]) + 10
# lowerColor2 = np.array([232, 162, 0]) - 10
# upperColor2 = np.array([232, 162, 0]) + 10

# # Create masks for the colors
# mask1 = cv2.inRange(image, lowerColor1, upperColor1)
# mask2 = cv2.inRange(image, lowerColor2, upperColor2)
# combinedMask = cv2.bitwise_or(mask1, mask2)
# resultImage = cv2.bitwise_and(image, image, mask=combinedMask)

# # Convert to grayscale
# gray = cv2.cvtColor(resultImage, cv2.COLOR_BGR2GRAY)

# # Find contours (vectors) in the masked image
# contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Convert contours to GeoJSON format
# features = []
# for contour in contours:
#     # Reshape contour to (x, y) points
#     polygon = contour.reshape(-1, 2).tolist()

#     # Transform pixel coordinates to geographic coordinates
#     transformed_polygon = []
#     for point in polygon:
#         pixel_x, pixel_y = point
#         # Get geographic coordinates from pixel coordinates
#         geo_x, geo_y = geo_transform * (pixel_x, pixel_y)

#         # Append the transformed coordinates
#         transformed_polygon.append([geo_x, geo_y])

#     # Check if any coordinates are invalid before creating GeoJSON
#     if all(-90 <= coord[1] <= 90 for coord in transformed_polygon):  # coord[1] is latitude
#         # Create GeoJSON feature
#         feature = {
#             "type": "Feature",
#             "geometry": {
#                 "type": "Polygon",
#                 "coordinates": [transformed_polygon]
#             },
#             "properties": {}
#         }
#         features.append(feature)

# geojson = {
#     "type": "FeatureCollection",
#     "features": features
# }

# # Save GeoJSON to a file
# geojson_path = r'C:\Users\91844\Desktop\6Simplex\New folder\extracted_blue_parts_reprojected.geojson'
# with open(geojson_path, 'w') as f:
#     json.dump(geojson, f)

# print(f"GeoJSON file saved at: {geojson_path}")

# # Visualizations
# contourImage = np.zeros_like(image)
# cv2.drawContours(contourImage, contours, -1, (0, 255, 0), 2)

# imageRgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# resultImageRgb = cv2.cvtColor(resultImage, cv2.COLOR_BGR2RGB)
# contourImageRgb = cv2.cvtColor(contourImage, cv2.COLOR_BGR2RGB)

# plt.figure(figsize=(10, 8))
# plt.subplot(2, 3, 1)
# plt.title('Original Image')
# plt.imshow(imageRgb)
# plt.axis('off')

# plt.subplot(2, 3, 2)
# plt.title('Result Image')
# plt.imshow(resultImageRgb)
# plt.axis('off')

# plt.subplot(2, 3, 3)
# plt.title('Vectorized Contours')
# plt.imshow(contourImageRgb)
# plt.axis('off')

# plt.show()
# --------------------------------------------------------------------------
import cv2
import numpy as np
import json
import rasterio
from osgeo import osr
from matplotlib import pyplot as plt

# Load the reprojected GeoTIFF image
file_path = r'C:\Users\91844\Desktop\6Simplex\New folder\new_version_for_extraction\reprojected_geotiff_4326.tif'
image = cv2.imread(file_path)

if image is None:
    print(f"Failed to load image at {file_path}")
    exit(1)
else:
    print("Image loaded successfully, dimensions:", image.shape)

# Get image dimensions
height, width, _ = image.shape

# Open the dataset with rasterio to get transformation info
with rasterio.open(file_path) as src:
    geo_transform = src.transform

# Define the color ranges for blue polygons
lowerColor1 = np.array([83, 195, 189]) - 10
upperColor1 = np.array([83, 195, 189]) + 10
lowerColor2 = np.array([232, 162, 0]) - 10
upperColor2 = np.array([232, 162, 0]) + 10

# Create masks for the colors
mask1 = cv2.inRange(image, lowerColor1, upperColor1)
mask2 = cv2.inRange(image, lowerColor2, upperColor2)
combinedMask = cv2.bitwise_or(mask1, mask2)

# Extract the blue parts from the image
resultImage = cv2.bitwise_and(image, image, mask=combinedMask)

# Check if the mask has any non-zero pixels
if np.sum(combinedMask) == 0:
    print("No blue areas detected in the image.")
else:
    print("Blue areas detected in the image.")

# Convert to grayscale
gray = cv2.cvtColor(resultImage, cv2.COLOR_BGR2GRAY)

# Find contours (vectors) in the masked image
contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Convert contours to GeoJSON format
features = []
for contour in contours:
    # Reshape contour to (x, y) points
    polygon = contour.reshape(-1, 2).tolist()

    # Transform pixel coordinates to geographic coordinates
    transformed_polygon = []
    for point in polygon:
        pixel_x, pixel_y = point
        # Get geographic coordinates from pixel coordinates
        geo_x, geo_y = geo_transform * (pixel_x, pixel_y)
        # Append the transformed coordinates
        transformed_polygon.append([geo_x, geo_y])

    # Check if any coordinates are invalid before creating GeoJSON
    if all(-90 <= coord[1] <= 90 for coord in transformed_polygon):  # coord[1] is latitude
        # Create GeoJSON feature for blue parts
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [transformed_polygon]  # Ensure coordinates are in the correct format
            },
            "properties": {
                "color": "blue"  # Indicating that the color is blue
            }
        }
        features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Save GeoJSON to a file
geojson_path = r'C:\Users\91844\Desktop\6Simplex\New folder\new_version_for_extraction\extracted_blue_parts.geojson'
with open(geojson_path, 'w') as f:
    json.dump(geojson, f)

print(f"GeoJSON file saved at: {geojson_path}")

# Optional Visualization
plt.figure(figsize=(12, 8))
plt.subplot(1, 3, 1)
plt.title('Original Image')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Mask')
plt.imshow(combinedMask, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Extracted Blue Parts')
plt.imshow(cv2.cvtColor(resultImage, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.show()
