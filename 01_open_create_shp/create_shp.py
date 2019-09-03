from osgeo import ogr,osr

shape = r"B:\curso_python_gis\data\shapefile.shp"

epsg = 4674

driver = ogr.GetDriverByName('ESRI Shapefile')

out_ds = driver.CreateDataSource(shape)

sr = osr.SpatialReference()
sr.ImportFromEPSG(epsg) 

layer = out_ds.CreateLayer(shape,sr,geom_type=ogr.wkbMultiPolygon)

field_name = ogr.FieldDefn("Name", ogr.OFTString)
field_name.SetWidth(24)
layer.CreateField(field_name)

layer_defn = ogr.Feature(layer.GetLayerDefn())

ring = ogr.Geometry(ogr.wkbLinearRing)
ring.AddPoint(-51, -1)
ring.AddPoint(-50, -1)
ring.AddPoint(-50, -2)
ring.AddPoint(-51, -2)
ring.AddPoint(-51, -1)

poly = ogr.Geometry(ogr.wkbPolygon)
poly.AddGeometry(ring)

feature = ogr.Feature(layer.GetLayerDefn())
feature.SetField("Name", 'my first polygon')

feature.SetGeometry(poly)

layer.CreateFeature(feature)

feature = out_ds = None


