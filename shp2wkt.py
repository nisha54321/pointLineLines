import sys, os
from osgeo import ogr

input = ogr.Open("/home/bisag/Documents/narmada_contour/layer/lines.shp")

layer_in = input.GetLayer()
layer_in.ResetReading()
feature_in = layer_in.GetNextFeature()
outfile = open("/home/bisag/Documents/narmada_contour/layer/lines.txt","w")
while feature_in is not None:

    geom = feature_in.GetGeometryRef()

    geom_name = geom.GetGeometryName()

    print(geom_name)

    wkt = geom.ExportToWkt()
    print(type(wkt))
    outfile.write(wkt + '\n')

    feature_in = layer_in.GetNextFeature()


# import shapefile
# import pygeoif
# r = shapefile.Reader("/home/bisag/Documents/narmada_contour/layer/lines.shp")

# g=[]

# for s in r.shapes():
#     g.append(pygeoif.geometry.as_shape(s)) 

# m = pygeoif.MultiLineString(g)
# wkt1 = str(m.wkt)

# f = open("/home/bisag/Documents/narmada_contour/layer/lines.wkt","w")
# f.write(wkt1)



# from osgeo import ogr
# # myfile = ogr.Open("/home/bisag/Documents/narmada_contour/Narmada_Contour.shp")#input Shapefile
# myfile = ogr.Open("/home/bisag/Documents/narmada_contour/line.shp")#input Shapefile

# myshape = myfile.GetLayer(0)
# feature = myshape.GetFeature(0)
# myfeature = feature.ExportToJson()
# import json

# myfeature = json.loads(myfeature)
# import geodaisy.converters as convert
# wkt_str = convert.geojson_to_wkt(myfeature['geometry'])
# outfile = open("/home/bisag/Documents/narmada_contour/line.wkt",'w')#output WKT file
# outfile.write(wkt_str)
# outfile.close()
