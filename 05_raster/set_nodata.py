import os
from subprocess import call

imgpath = r'D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\mosaico'

for root,dirs,files in os.walk(imgpath):
    for arq in files:
        if root != imgpath:
            continue
        if arq.endswith(".TIF"):
            print root,arq
            arq_path = os.path.join(root,arq)
            call("gdal_edit -a_nodata 0 {}".format(arq_path),shell=True)