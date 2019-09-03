import ogr,osr

shp = r"B:\curso_python_gis\data\intersection.shp"

#supports Datums 4674 or 4326 
epsg = 4674

def create_shp(path,epsg,geom_type):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    out_ds = driver.CreateDataSource(path)
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(epsg) 
    layer = out_ds.CreateLayer(path,sr,geom_type=geom_type)
    return out_ds,layer

def utm_getZone(longitude):
    return (int(1+(longitude+180.0)/6.0))

def utm_isNorthern(latitude):
    if (latitude < 0.0):
        return -1
    else:
        return 1

def get_utm_epsg(fuse,epsg):
    #fuses = [18,19,20,21,22,23,24,25]
    epsg_dic = {}
    if epsg == 4326:
        for fuso in range(18,26):
            epsgS = int('327{}'.format(fuso))
            epsgN = int('326{}'.format(fuso))
            epsg_dic[-fuso] = epsgS
            epsg_dic[fuso] = epsgN
    elif epsg == 4674:
        codN = 72
        codS = 78
        for fuso in range(18,26):
            epsgS = int('319{}'.format(codS))
            epsgN = int('319{}'.format(codN))
            epsg_dic[-fuso] = epsgS
            epsg_dic[fuso] = epsgN
            codN += 1
            codS += 1
    return epsg_dic[fuse]

def main():
    ds = ogr.Open(shp)
    layer = ds.GetLayer()
    layer_defn = layer.GetLayerDefn()

    x,y = [],[]
    for feature in layer:
        geom = feature.geometry()
        centroid = geom.Centroid()
        x.append(centroid.GetX())
        y.append(centroid.GetY())
    xm = float(sum(x))/len(x)
    ym = float(sum(y))/len(y)

    fuse = utm_getZone(xm)
    north = utm_isNorthern(ym)

    fuse = fuse*north

    utm_epsg = get_utm_epsg(fuse,epsg)

    source = layer.GetSpatialRef()

    target = osr.SpatialReference()
    target.ImportFromEPSG(utm_epsg)

    transform_to_utm = osr.CoordinateTransformation(source, target)

    out_shp = shp.replace('.shp','_rep.shp')
    out_ds,out_layer = create_shp(out_shp,utm_epsg,ogr.wkbMultiPolygon)

    layer.ResetReading()

    for feature in layer:
        geom = feature.geometry()
        geom.Transform(transform_to_utm)

        out_feature = ogr.Feature(layer_defn)
        out_feature.SetGeometry(geom)

        out_layer.CreateFeature(out_feature)

    feature = out_ds = ds = None


if __name__ == "__main__":
    main()