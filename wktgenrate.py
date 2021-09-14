# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/bisag/.local/lib/python3.6/site-packages/')
path = ['/home/bisag/.var/app/org.qgis.qgis/data/QGIS/QGIS3/profiles/default/python/plugins/qproto', '/home/bisag/.var/app/org.qgis.qgis/data/QGIS/QGIS3/profiles/default/python/plugins/csv_tools', '/app/share/qgis/python', '/home/bisag/.var/app/org.qgis.qgis/data/QGIS/QGIS3/profiles/default/python', '/home/bisag/.var/app/org.qgis.qgis/data/QGIS/QGIS3/profiles/default/python/plugins', '/app/share/qgis/python/plugins', '/usr/lib/python38.zip', '/usr/lib/python3.8', '/usr/lib/python3.8/lib-dynload', '/usr/lib/python3.8/site-packages', '/app/lib/python3.8/site-packages', '/app/lib/python3.8/site-packages/numpy-1.19.2-py3.8-linux-x86_64.egg', '/app/lib/python3.8/site-packages/MarkupSafe-1.1.1-py3.8-linux-x86_64.egg', '/home/bisag/.var/app/org.qgis.qgis/data/QGIS/QGIS3/profiles/default/python', '/home/bisag/.local/lib/python3.6/site-packages/', '.', '/home/bisag/.var/app/org.qgis.qgis/data/QGIS/QGIS3/profiles/default/python/plugins/QuickMultiAttributeEdit3/forms']

for i in path:
    sys.path.append(i)

from qgis.gui import QgsMapToolEmitPoint
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QCheckBox, QListView, QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets 
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import QgsVectorLayer,QgsProject, QgsGeometry, QgsFeature, QgsSymbol, QgsSingleSymbolRenderer, QgsDataSourceUri, QgsPointXY, QgsPoint, QgsVectorFileWriter
from osgeo import ogr
import shapefile
from qgis.PyQt.QtWidgets import QAction
import psycopg2
import sys 
#import traceback
import logging
import math    
from random import randrange
from qgis import processing
import os
import time
from qgis.gui import QgsMapToolIdentifyFeature
import re, os.path
from osgeo import ogr

from qgis.core import QgsApplication, QgsProject, QgsVectorLayer, QgsVectorLayerTemporalProperties
from PyQt5.QtCore import QFileInfo
# Initialize Qt resources from file resources.py

import os.path

from PyQt5 import QtWidgets, QtGui

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .wkt_generate_dialog import WktGenerateDialog
import os.path


class WktGenerate:
    x = 0.0
    y = 0.0 
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'WktGenerate_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Wkt_Generate')

       
        self.first_start = None

    def tr(self, message):

        return QCoreApplication.translate('WktGenerate', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):

        icon_path = ':/plugins/wkt_generate/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'wkt generator'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.first_start = True


    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Wkt_Generate'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
       
        if self.first_start == True:
            self.first_start = False
            self.dlg = WktGenerateDialog()

        xy = []
        def display_point( pointTool ): 
            coorx = float('{}'.format(pointTool[0]))
            coory = float('{}'.format(pointTool[1]))
            print(coorx, coory)
            self.x = coorx
            self.y = coory
            xy.append(coorx)
            xy.append(coory)
            
            
        canvas = self.iface.mapCanvas()   
        pointTool = QgsMapToolEmitPoint(canvas)
        pointTool.canvasClicked.connect( display_point )
        canvas.setMapTool( pointTool )

        def point1():
            #draw point
    
            vl = QgsVectorLayer("Point?crs=EPSG:4326", "Point", "memory")

            vl.renderer().symbol().setSize(3.5)
            vl.renderer().symbol().setColor(QColor("green"))
            vl.triggerRepaint()

            f = QgsFeature()
            print(self.x, self.y)
            f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(self.x,self.y)))
            pr = vl.dataProvider()

            pr.addFeature(f)
            vl.updateExtents() 
            vl.updateFields() 
            QgsProject.instance().addMapLayers([vl])
            
            #save point 
            sp = "/home/bisag/Documents/narmada_contour/layer/point.shp"
            QgsVectorFileWriter.writeAsVectorFormat(vl, sp, "UTF-8", vl.crs() , "ESRI Shapefile")

            #convert wkt
            myfile = ogr.Open(sp)#input Shapefile

            myshape = myfile.GetLayer(0)
            feature = myshape.GetFeature(0)
            myfeature = feature.ExportToJson()
            import json

            myfeature = json.loads(myfeature)
            import geodaisy.converters as convert
            wkt_str = convert.geojson_to_wkt(myfeature['geometry'])
            outfile = open("/home/bisag/Documents/narmada_contour/wkt/point.txt",'w')#output WKT file
            outfile.write(wkt_str)
            outfile.close()

        def line1():
            start_point = QgsPoint(xy[-4], xy[-3])
            end_point = QgsPoint(xy[-2], xy[-1])
            print(xy)
            
            #draw line
            v_layer = QgsVectorLayer('LineString?crs=epsg:4326', 'line', 'memory')
            pr = v_layer.dataProvider()
            seg = QgsFeature()
            seg.setGeometry(QgsGeometry.fromPolyline([start_point, end_point]))
            pr.addFeatures([ seg ])
            QgsProject.instance().addMapLayers([v_layer])

            
            QgsVectorFileWriter.writeAsVectorFormat(v_layer, "/home/bisag/Documents/narmada_contour/layer/line.shp", "UTF-8", v_layer.crs() , "ESRI Shapefile")
            myfile = ogr.Open("/home/bisag/Documents/narmada_contour/layer/line.shp")#input Shapefile

            myshape = myfile.GetLayer(0)
            feature = myshape.GetFeature(0)
            myfeature = feature.ExportToJson()
            import json

            myfeature = json.loads(myfeature)
            import geodaisy.converters as convert
            wkt_str = convert.geojson_to_wkt(myfeature['geometry'])
            outfile = open("/home/bisag/Documents/narmada_contour/wkt/line.txt",'w')#output WKT file
            outfile.write(wkt_str)
            outfile.close()

        def lines():
            processing.run("native:extractbylocation", {'INPUT':'/home/bisag/Documents/narmada_contour/Narmada_Contour.shp',
                                        'PREDICATE':[0],
                                        'INTERSECT':'/home/bisag/Documents/narmada_contour/layer/line.shp',
                                    'OUTPUT':'/home/bisag/Documents/narmada_contour/layer/lines.shp'})

            layer = QgsVectorLayer("/home/bisag/Documents/narmada_contour/layer/lines.shp", "lines", "ogr")
            QgsProject.instance().addMapLayer(layer)

            input = ogr.Open("/home/bisag/Documents/narmada_contour/layer/lines.shp")

            layer_in = input.GetLayer()
            layer_in.ResetReading()
            feature_in = layer_in.GetNextFeature()
            outfile = open("/home/bisag/Documents/narmada_contour/wkt/lines.txt","w")
            while feature_in is not None:
                geom = feature_in.GetGeometryRef()
                geom_name = geom.GetGeometryName()
                print(geom_name)
                wkt = geom.ExportToWkt()
                outfile.write(wkt + '\n')
                feature_in = layer_in.GetNextFeature()

        self.dlg.pushButton_point.clicked.connect(point1)
        self.dlg.pushButton_line.clicked.connect(line1)
        self.dlg.pushButton_lines.clicked.connect(lines)
        
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
