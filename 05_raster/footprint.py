import os
from subprocess import call

img_path = r'D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00'

for root,dirs,files in os.walk(img_path):
  for img in files:
    if img.lower().endswith('.tif'):

      black = img[:-4]+"_black.tif"
      foot = img[:-4]+"_foot.shp"

      imgp = os.path.join(root,img)
      blackp = os.path.join(root,black)
      footp = os.path.join(root,foot)

      call("gdal_translate -co compress=lzw -b 1 -ot byte -scale 1 1 {} {}".format(imgp,blackp),shell=True)
      call("gdal_polygonize {} -b 1".format(blackp,footp),shell=True)
      call('del /q {}'.format(blackp),shell=True)
