#!/usr/bin/env python

# import libraries
import argparse
import numpy as np
import rasterio
from xml.dom import minidom
import time
start_time = time.time()

# Have user define input bands and output filename
parser = argparse.ArgumentParser(description='GeoTiff Planet Multispectral Image Radiance to TOA Reflectance Conversion Script')
parser.add_argument('-in', '--input_file', help='Planet Analytic.tif MS image file', required=True)

args = parser.parse_args()

filename = args.input_file
xml_fn = filename[:-4]+'_metadata.xml'
out_fn = filename[:-4]+'_refl.tif'

print("Filename is: ", filename)
print("XML is: ", xml_fn)
print("Out filename is: ", out_fn)

# Load all bands as numpy arrays - note all PlanetScope 4-band images have band order BGRN
with rasterio.open(filename) as src:
# Alternative method, seems to take the same amount of time
#     f=src.read()
#     band_blue_radiance = f[0, :, :]
#     band_green_radiance = f[1, :, :]
#     band_red_radiance = f[2, :, :]
#     band_nir_radiance = f[3, :, :]
    
    band_blue_radiance = src.read(1)
    band_green_radiance = src.read(2)
    band_red_radiance = src.read(3)
    band_nir_radiance = src.read(4)
    
# print('Shapes are: ', band_blue_radiance.shape, '\n',
#      band_green_radiance.shape, '\n',
#      band_red_radiance.shape, '\n',
#      band_nir_radiance.shape, '\n',)
    
xmldoc = minidom.parse(xml_fn)
nodes = xmldoc.getElementsByTagName("ps:bandSpecificMetadata")

# XML parser refers to bands by numbers 1-4
coeffs = {}
for node in nodes:
    bn = node.getElementsByTagName("ps:bandNumber")[0].firstChild.data
    if bn in ['1', '2', '3', '4']:
        i = int(bn)
        value = node.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
        coeffs[i] = float(value)

print("Conversion coefficients:", coeffs)


# Multiply the Digital Number (DN) values in each band by the TOA reflectance coefficients
band_blue_reflectance = band_blue_radiance * coeffs[1]
band_green_reflectance = band_green_radiance * coeffs[2]
band_red_reflectance = band_red_radiance * coeffs[3]
band_nir_reflectance = band_nir_radiance * coeffs[4]

# print("Red band radiance is from", np.amin(band_red_radiance), "to", np.amax(band_red_radiance))
# print("Red band reflectance is from", np.amin(band_red_reflectance), "to", np.amax(band_red_reflectance))

# Set spatial characteristics of the output object to mirror the input
kwargs = src.meta
kwargs.update(
    dtype=rasterio.uint16,
    count = 4)
# print("Before SCALING, red band reflectance is from", np.amin(band_red_reflectance), "to", np.amax(band_red_reflectance))


# Here we include a fixed scaling factor. This is common practice.
scale = 10000
blue_ref_scaled = scale * band_blue_reflectance
green_ref_scaled = scale * band_green_reflectance
red_ref_scaled = scale * band_red_reflectance
nir_ref_scaled = scale * band_nir_reflectance
# print("After SCALING, red band reflectance is from", np.amin(red_ref_scaled), "to", np.amax(red_ref_scaled))

# Write band calculations to a new raster file
with rasterio.open(out_fn, 'w', **kwargs) as dst:
        dst.write_band(1, blue_ref_scaled.astype(rasterio.uint16))
        dst.write_band(2, green_ref_scaled.astype(rasterio.uint16))
        dst.write_band(3, red_ref_scaled.astype(rasterio.uint16))
        dst.write_band(4, nir_ref_scaled.astype(rasterio.uint16))
        
elapsed_time = time.time() - start_time
print("Total time elapsed for toa_calc.py is:", "{0:.4}".format(elapsed_time), "seconds")