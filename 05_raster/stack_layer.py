from subprocess import call

raster = r'D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180762015195LGN00\LC82180762015195LGN00_B'

rasterout = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00\LC82180762015195LGN00_stack.TIF"

call("gdal_merge -separate {}2.TIF {}3.TIF {}4.TIF {}5.TIF -o {}".format(raster,raster,raster,raster,rasterout),shell=True)