import rasterio
from rasterio.plot import show

# Path to the annual mean Kd490 TIFF file
file_path = './data/light/Kd490_Annual_Mean.tif.ovr'

# Open the raster file using rasterio
with rasterio.open(file_path) as src:
    # Read the raster data
    annual_mean_kd490 = src.read(1)
    
    # Plot the raster data
    show(annual_mean_kd490, title='Annual Mean Kd490')

    # Additional analysis can be performed here depending on your needs
    # For example, calculating statistics or integrating with other data layers
