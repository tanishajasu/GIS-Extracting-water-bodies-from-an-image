from osgeo import gdal

# Open the GeoTIFF file
file_path = 'C:/Users/91844/Desktop/6Simplex/New folder/new_version_for_extraction/reprojected_geotiff_4326.tif'
dataset = gdal.Open(file_path)

# Get the GeoTransform
geotransform = dataset.GetGeoTransform()

# Image size
x_size = dataset.RasterXSize
y_size = dataset.RasterYSize

# Calculate the center pixel coordinates
center_x = x_size // 2
center_y = y_size // 2

# Calculate the geographic coordinates (longitude, latitude) of the center
center_longitude = geotransform[0] + center_x * geotransform[1] + center_y * geotransform[2]
center_latitude = geotransform[3] + center_x * geotransform[4] + center_y * geotransform[5]

# Print the center coordinates
print(f"Center Coordinates (Longitude, Latitude): ({center_longitude}, {center_latitude})")


# output
# Latitude: 79.0916066392212
# Longitude: 21.161838430737205