from osgeo import ogr,osr

#more on https://pcjericks.github.io/py-gdalogr-cookbook/

shape = r"B:\curso_pygis2_data\shapefile_2.shp"

epsg = 4674

points = [[-51, -1],[-50, -1],[-50, -2],[-51, -2],[-51, -1]]

fields_str = ['name','obs']
fields_float = ['x','y']
fields_int = ['id','count']

def create_shp(path,epsg,geom_type):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    out_ds = driver.CreateDataSource(path)
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(epsg)
    layer = out_ds.CreateLayer(path,sr,geom_type=geom_type)
    return out_ds,layer

def create_fields_str(fields,layer,width=150):
    for field_name in fields:
        field = ogr.FieldDefn(field_name, ogr.OFTString)
        field.SetWidth(width)
        layer.CreateField(field)

def create_fields_int(fields,layer):
    for field_name in fields:
        field = ogr.FieldDefn(field_name, ogr.OFTInteger)
        layer.CreateField(field)

def create_fields_float(fields,layer,width=31,precision=5):
    for field_name in fields:
        field = ogr.FieldDefn(field_name, ogr.OFTReal)
        field.SetWidth(width)
        field.SetPrecision(precision)
        layer.CreateField(field)

def create_polygon(points):
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for point in points:
        print(point)
        ring.AddPoint(point[0],point[1])
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly

def main():
    out_ds,layer = create_shp(shape,epsg,ogr.wkbMultiPolygon)
    
    create_fields_str(fields_str,layer)
    create_fields_float(fields_float,layer)
    create_fields_int(fields_int,layer)

    layer_defn = layer.GetLayerDefn()

    poly = create_polygon(points)

    feature = ogr.Feature(layer_defn)
    feature.SetField(fields_str[0], 'my first polygon')
    feature.SetGeometry(poly)

    layer.CreateFeature(feature)

    feature = out_ds = None

if __name__ == "__main__":
    main()
    print('legal')