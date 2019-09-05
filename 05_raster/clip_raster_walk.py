from subprocess import call
import os


rasterpath = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00"

cutline = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_vetor\carrancas.shp"


def clip_raster(rasterin,rasterout,cutline):
    call("gdalwarp -cutline {} {} {}".format(cutline,rasterin,rasterout),shell=True)

for root,dirs,files in os.walk(rasterpath):
    for arq in files:
        if arq.endswith(".TIF"):
            rasterin = os.path.join(root,arq)
            rasteroutnam = arq[:-4]+"_clip.TIF"
            rasterout = os.path.join(root,rasteroutnam)
            clip_raster(rasterin,rasterout,cutline)