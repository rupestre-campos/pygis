import ogr

shape = r"B:\curso_python_gis\data\shapefile.shp"

ds = ogr.Open(shape)

layer = ds.GetLayer()

feature = layer.GetNextFeature()

name = feature.GetField('Name')

print(name)

geom = feature.geometry()
geom.GetPointCount()
geom.GetGeometryCount()

geom.GetGeometryType()
geom.GetArea()
geom.Buffer(1).GetArea()


geom_line = geom.GetGeometryRef(0)
geom_line.GetGeometryType()
geom_line.GetPointCount()

for point in range(0, geom_line.GetPointCount()):
    pt = geom_line.GetPoint(point)
    print("{} POINT ({} {})".format(point, pt[0], pt[1]))

ds = None