import ogr,osr
from collections import defaultdict

shp = r"B:\curso_python_gis\data\shapefile_4.shp"

databaseUser = "****"
databasePW = "****"
databaseServer = "*****"
databaseName = "****"

schema_table = 'python_gis.grid_sat'

connString = "PG: host={} dbname={} user={} password={}".format(databaseServer,databaseName,databaseUser,databasePW)


def create_shp(path,srs,geom_type):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    out_ds = driver.CreateDataSource(path)
    layer = out_ds.CreateLayer(path,srs,geom_type=geom_type)
    return out_ds,layer

def create_fields_str(fields,layer,width=150):
    for field_name in fields:
        field = ogr.FieldDefn(field_name, ogr.OFTString)
        field.SetWidth(width)
        layer.CreateField(field)

def main():
    ds = ogr.Open(shp)
    layer = ds.GetLayer()
    
    ds_sat = ogr.Open(connString)
    layer_sat = ds_sat.GetLayer(schema_table)

    out_shp = shp.replace('.shp','_uf.shp')

    srs = layer.GetSpatialRef()
    out_ds,out_layer = create_shp(out_shp,srs,ogr.wkbMultiPolygon)
    create_fields_str(['tile_id','sat'],out_layer)
    layer_defn = layer_sat.GetLayerDefn()

    for feat in layer:
        geom = feat.geometry()
        layer_sat.SetSpatialFilter(geom)

        info = defaultdict(list)
        for tile in layer_sat:
            tile_id = tile.GetField('tile_id')
            sensor = tile.GetField('sat')

            info[sensor].append(tile_id)

            feature = ogr.Feature(layer_defn)
            feature.SetGeometry(tile.geometry())
            feature.SetField('tile_id',tile_id)
            feature.SetField('sat',sensor)
            out_layer.CreateFeature(feature)
            feature = None

    out_ds = ds = None

    for i in info:
        print i
        print info[i]


if __name__ == "__main__":
    main()