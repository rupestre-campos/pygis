import ogr,osr

out_shp = r"B:\curso_python_gis\data\class_diss.shp"


databaseUser = "***"
databasePW = "****"
databaseServer = "****"
databaseName = "****"

schema_table = 'python_gis.class'

connString = "PG: host={} dbname={} user={} password={}".format(databaseServer,databaseName,databaseUser,databasePW)

def main():
    dissolve(out_shp,connString,schema_table)

def dissolve(output,connString, schema_table, field=0):
    geomClassDic = {}
    dissolveDic = {}
    ds = ogr.Open(connString)
    lyr = ds.GetLayer(schema_table)

    drv = ogr.GetDriverByName("ESRI Shapefile")
    out_ds = drv.CreateDataSource(output)
    out_lyr = out_ds.CreateLayer(output, lyr.GetSpatialRef(),lyr.GetGeomType())

    if not field == 0:
        new_field = ogr.FieldDefn(field, ogr.OFTString)
        new_field.SetWidth(150)
        out_lyr.CreateField(new_field)
        defn = out_lyr.GetLayerDefn()
        classes = set()
        for feat in lyr:
            #if feat.geometry():
            field_classes = feat.GetField(field)
            classes.add(field_classes)
        lyr.ResetReading()
        for claz in classes:
            filt = "{} = '{}'".format(field, claz)
            lyr.SetAttributeFilter(filt)
            multi = ogr.Geometry(ogr.wkbMultiPolygon)
            out_feat = ogr.Feature(defn)
            for feat in lyr:
                multi.AddGeometry(feat.geometry().Buffer(0))
            union = multi.UnionCascaded()
            #buff = multi.Buffer(0)
            out_feat.SetGeometry(union)
            out_feat.SetField(field, str(claz))
            #out_feat.SetField("area", buff.GetArea())
            out_lyr.CreateFeature(out_feat)
            out_feat = None
    else:
        defn = out_lyr.GetLayerDefn()
        multi = ogr.Geometry(ogr.wkbMultiPolygon)
        for feat in lyr:
            geom = feat.geometry()
            if geom.GetGeometryType() == ogr.wkbMultiPolygon:
                for polygon in geom:
                    multi.AddGeometry(polygon)
            else:
                multi.AddGeometry(geom)
        print('geom added, now union...')
        union = multi.UnionCascaded()
        out_feat = ogr.Feature(defn)
        out_feat.SetGeometry(union)
        out_lyr.CreateFeature(out_feat)
        out_feat = None

    out_ds = ds = None

if __name__ == "__main__":
    main()