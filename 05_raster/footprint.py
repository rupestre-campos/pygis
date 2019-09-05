import os
from subprocess import call
path = r'D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00'

img = 'LC82180752015243LGN00_stack_10m.TIF'
black = img[:-4]+"_black.tif"
foot = img[:-4]+"_foot.shp"

imgp = os.path.join(path,img)
blackp = os.path.join(path,black)
footp = os.path.join(path,foot)

call("gdal_translate -co compress=lzw -b 1 -ot byte -scale 1 1 {} {}".format(imgp,blackp),shell=True)
call("gdal_polygonize {} -b 1".format(blackp,footp),shell=True)