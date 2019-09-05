from subprocess import call
from osgeo import gdal,osr

rasterin = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00\LC82180752015243LGN00_B8.TIF"
rasterout = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00\LC82180752015243LGN00_B8_4674.TIF"

ds = gdal.Open(rasterin)

prj = ds.GetProjection()
srs = osr.SpatialReference(wkt=prj)
fuse = srs.GetUTMZone()

epsg_dic = {}
epsg_dic[-18] = 32718
epsg_dic[-19] = 32719
epsg_dic[-20] = 32720
epsg_dic[-21] = 32721
epsg_dic[-22] = 32722
epsg_dic[23] = 32723
epsg_dic[-24] = 32724
epsg_dic[-25] = 32725
epsg_dic[18] = 32618
epsg_dic[19] = 32619
epsg_dic[20] = 32620

epsg = epsg_dic[fuse]


def reprojetar(rasterin,rasterout,epsg):
    call("gdalwarp -t_srs EPSG:{} {} {}".format(epsg,rasterin,rasterout),shell=True)

reprojetar(rasterin,rasterout,4674)