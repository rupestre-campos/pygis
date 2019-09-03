import ogr,osr

shp = r"B:\CNN\v0.34\001_065\class_19_001_065.shp"

def main():
    dissolve(shp)

def dissolve(input_shp, field=0):
    geomClassDic = {}
    dissolveDic = {}
    ds = ogr.Open(input_shp)
    lyr = ds.GetLayer()
    drv = ogr.GetDriverByName(ds.GetDriver().GetName())
    output = input_shp.replace('.shp','_diss.shp')
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
                multi = multi.Union(feat.geometry())
            #buff = multi.Buffer(0)
            out_feat.SetGeometry(multi)
            out_feat.SetField(field, str(claz))
            #out_feat.SetField("area", buff.GetArea())
            out_lyr.CreateFeature(out_feat)
            out_feat = None
    else:
        defn = out_lyr.GetLayerDefn()
        multi = ogr.Geometry(ogr.wkbMultiPolygon)
        for feat in lyr:
            multi = multi.Union(feat.geometry())

        out_feat = ogr.Feature(defn)
        out_feat.SetGeometry(multi)
        out_lyr.CreateFeature(out_feat)
        out_feat = None

    out_ds = ds = None

if __name__ == "__main__":
    main()