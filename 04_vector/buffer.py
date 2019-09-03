import ogr,osr

shp = r"B:\curso_python_gis\data\intersection_rep.shp"

segments = 3

def create_shp(path,epsg,geom_type):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    out_ds = driver.CreateDataSource(path)
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(epsg) 
    layer = out_ds.CreateLayer(path,sr,geom_type=geom_type)
    return out_ds,layer


def main():
    ds = ogr.Open(shp)
    layer = ds.GetLayer()
    layer_defn = layer.GetLayerDefn()

    out_shp = shp.replace('.shp','_buffer7.shp')
    out_ds,out_layer = create_shp(out_shp,31982,ogr.wkbMultiPolygon)

    for feat in layer:
        geom = feat.geometry()
        buffer = geom.Buffer(500,segments)


        feature = ogr.Feature(layer_defn)
        feature.SetGeometry(buffer)

        out_layer.CreateFeature(feature)

    feature = out_ds = None


if __name__ == "__main__":
    main()