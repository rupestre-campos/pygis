import Vector


v1 = Vector.Vector(r"B:\curso_python_gis\data\shapefile.shp")
print v1.collumns
#['name', 'obs', 'x', 'y', 'id', 'count']
v3 = Vector.Vector(r"B:\curso_python_gis\data\shapefile_4.shp")
print v3.epsg
print v3.geom_type

points = [[-51, -1],[-50, -1],[-50, -2],[-51, -2],[-51, -1]]
atributes = {'name':'my polygon','obs':'teste','x':1.3321,'y':3.5554,'id':1,'count':432324356}
print atributes['name'],atributes['x']

fields_str = ['name','obs']
fields_float = ['x','y']
fields_int = ['id','count']

v3.create_fields_str(fields_str)
v3.create_fields_float(fields_float)
v3.create_fields_int(fields_int)

v3.create_polygon(points,atributes)

v4 = Vector.Vector(r"B:\curso_python_gis\data\intersection.shp")
points = [[-51, -1],[-50, -1],[-50, -2],[-51, -2],[-51, -1]]
points2 = [[-50.5, -1],[-49.5, -1],[-49.5, -2],[-50.5, -2],[-50.5, -1]]

v4.create_polygon(points)
v4.create_polygon(points2)