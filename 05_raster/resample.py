from subprocess import call

rasterin = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00\LC82180752015243LGN00_stack.TIF"
rasterout = r"D:\Arquivos_GEO_CKC\curso_semad\bases_de_dados\base_raster\LC82180752015243LGN00\LC82180752015243LGN00_stack_10m.TIF"

call("gdalwarp -r bilinear -tr 10 10 {} {}".format(rasterin,rasterout),shell=True)