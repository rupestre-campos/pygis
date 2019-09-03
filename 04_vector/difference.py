import ogr,osr

shp = r"B:\curso_python_gis\data\intersection.shp"

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


    feat1 = layer.GetNextFeature()
    feat1_geom = feat1.geometry()

    feat2 = layer.GetNextFeature()
    feat2_geom = feat2.geometry()

    out_shp = shp.replace('.shp','_difference.shp')
    out_ds,out_layer = create_shp(out_shp,4674,ogr.wkbMultiPolygon)

    diff = feat1_geom.Difference(feat2_geom)

    feature = ogr.Feature(layer_defn)
    feature.SetGeometry(diff)

    out_layer.CreateFeature(feature)

    feature = out_ds = None


if __name__ == "__main__":
    main()