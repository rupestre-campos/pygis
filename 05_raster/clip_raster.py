from subprocess import call
from osgeo import gdal,osr

rasterin = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00\LC82180752015243LGN00_B8.TIF"
rasterout = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00\LC82180752015243LGN00_B8_clip.TIF"
cutline = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_vetor\carrancas.shp"


def clip_raster(rasterin,rasterout,cutline):
    call("gdalwarp -cutline {} {} {}".format(cutline,rasterin,rasterout),shell=True)

clip_raster(rasterin,rasterout,cutline)