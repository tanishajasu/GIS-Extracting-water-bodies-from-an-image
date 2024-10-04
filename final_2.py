from osgeo import gdal

# Open the GeoTIFF file
file_path = 'C:/Users/91844/Desktop/6Simplex/New folder/new_version_for_extraction/reprojected_geotiff_4326.tif'
dataset = gdal.Open(file_path)

# Extract metadata
metadata = {
    'Driver': dataset.GetDriver().ShortName,
    'Size': (dataset.RasterXSize, dataset.RasterYSize),
    'Number of Bands': dataset.RasterCount,
    'Projection': dataset.GetProjection(),
    'GeoTransform': dataset.GetGeoTransform(),
    'Metadata': dataset.GetMetadata(),
}

for key, value in metadata.items():
    print(f"{key}: {value}")
