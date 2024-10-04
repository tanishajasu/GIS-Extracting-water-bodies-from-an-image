import os
from osgeo import gdal, osr

# Open the source GeoTIFF file
file_path = 'C:/Users/91844/Desktop/6Simplex/New folder/geotiff_2409.tif'
dataset = gdal.Open(file_path)

# Define the target CRS (EPSG:4326 - WGS 84)
target_crs = osr.SpatialReference()
target_crs.ImportFromEPSG(4326)

# Check if the directory exists, and create it if necessary
output_dir = 'C:/Users/91844/Desktop/6Simplex/New folder/new_version_for_extraction/'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set the output file path
output_file = os.path.join(output_dir, 'reprojected_geotiff_4326.tif')

# Reproject the GeoTIFF
options = gdal.WarpOptions(dstSRS='EPSG:4326')
gdal.Warp(output_file, dataset, options=options)

print(f"Reprojected GeoTIFF saved at: {output_file}")
