import os
from subprocess import call

path = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\mosaico"

raster = 'mosaico_landsat.tif'
outRaster = 'mosaico_landsat_ndvi.tif'

raster_p = os.path.join(path,raster)
outRaster_p = os.path.join(path,outRaster)


call('gdal_calc -A {} --A_band=3 -B {} --B_band=4 --type=Float32 --outfile={} --calc="100*(1+((B.astype(float)-A)/(B.astype(float)+A)))"'.format(raster_p,raster_p,outRaster_p),shell=True)