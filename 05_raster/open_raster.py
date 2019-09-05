from osgeo import gdal


raster = r"C:\monitoramento_kfw\mapeamento\MT\2230804\2230804_lt05_224072_20080821.dat"
ds = gdal.Open(raster)

print ds.GetMetadata()
cols = ds.RasterXSize
rows = ds.RasterYSize

print (cols)
print (rows)

ds = None
