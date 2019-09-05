import os
from subprocess import call

path = r'D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\mosaico\bands_to_mosaic'

virt = "mosaico_hist.vrt"
mosaico = "mosaico_landsat_hist.tif"

virt_p =os.path.join(path,virt)
mos_p = os.path.join(path,mosaico)

call("gdalbuildvrt {} {}\\*.TIF".format(virt_p,path),shell=True)
call("gdalwarp {} {}".format(virt_p,mos_p),shell=True)