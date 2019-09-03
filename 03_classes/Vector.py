from osgeo import ogr,osr
import os
import atexit

class Vector:
    def __init__(self,path,epsg=0,geom_type='',edit=0):
        self.path = path
        self.ds = ''
        self.layer = ''
        self.edit = edit
        self.geom_type = geom_type
        if self.geom_type == '':
            self.geom_type = ogr.wkbMultiPolygon
        
        if not epsg == 0:
            self.epsg = epsg
        else:
            self.epsg = 4674
        
        if os.path.isfile(self.path):
            self.open_shp()
        else:
            self.create_shp()
        self.definition = self.layer.GetLayerDefn()
        self.collumns = []
        self.atribute_table()

        atexit.register(self.close_file)

    def close_file(self):
        self.ds = None

    def open_shp(self):
        self.ds = ogr.Open(self.path,self.edit)
        self.layer = self.ds.GetLayer()
        

    def create_shp(self):
        driver = ogr.GetDriverByName('ESRI Shapefile')
        sr = osr.SpatialReference()
        sr.ImportFromEPSG(self.epsg)
        self.ds = driver.CreateDataSource(self.path)
        self.layer = self.ds.CreateLayer(self.path,sr,geom_type=self.geom_type)
        

    def create_fields_str(self,fields,width=150):
        for field_name in fields:
            field = ogr.FieldDefn(field_name, ogr.OFTString)
            field.SetWidth(width)
            self.layer.CreateField(field)
            self.atribute_table()

    def create_fields_int(self,fields):
        for field_name in fields:
            field = ogr.FieldDefn(field_name, ogr.OFTInteger)
            self.layer.CreateField(field)
            self.atribute_table()

    def create_fields_float(self,fields,width=31,precision=5):
        for field_name in fields:
            field = ogr.FieldDefn(field_name, ogr.OFTReal)
            field.SetWidth(width)
            field.SetPrecision(precision)
            self.layer.CreateField(field)
            self.atribute_table()

    def create_polygon(self,points,atributes={}):
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for point in points:
            ring.AddPoint(point[0],point[1])
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        self.definition = self.layer.GetLayerDefn()
        feature = ogr.Feature(self.definition)
        if len(atributes) > 0:
            for key in atributes:
                feature.SetField(key,atributes[key])
        feature.SetGeometry(poly)
        self.layer.CreateFeature(feature)
        feature = None
    
    def atribute_table(self):
        self.collumns = []
        for n in range(self.definition.GetFieldCount()):
            fdefn = self.definition.GetFieldDefn(n)
            self.collumns.append(fdefn.name)