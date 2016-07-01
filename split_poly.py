"""
Splitting polygons into equal area parts
"""
from qgis.core import (QgsFeature, QgsGeometry,
                       QgsVectorLayer, QgsMapLayerRegistry,
                       QgsField,QgsPoint)
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import*
from qgis.utils import iface
import math

#this is required for the qgis script runner plugin
def run_script(iface):
    #global lineLayer
    #lineLayer = QgsVectorLayer("LineString?crs=3785", "split_line", "memory")
    eqsplit_inst = EqSplitPolygon()
    eqsplit_inst.debug = True
    eqsplit_inst.splitSelectedByNumber("Lakeview CEAs minus EAs",3, "a", 30)
    #QgsMapLayerRegistry.instance().addMapLayer(lineLayer)

class EqSplitPolygon:
    #def __init__(self,iface):
    def __init__(self):
        self.debug=False
        pass

    def splitSelectedByArea(self,targetArea,granulFactor,method="h",splitEven=True):
        global recurs
        recurs=0;
        layer = iface.mapCanvas().currentLayer()
        if layer:
            #Gets layer CRS for new layer
            crs=layer.crs().description()
            if self.debug: print "Starting, Layer crs: " + crs
            # Create a new memory layer and add an area attribute
            polyLayer = QgsVectorLayer("MultiPolygon?crs="+crs, "split_poly", "memory")
            polyLayer.dataProvider().addAttributes( [ QgsField("area", QVariant.Double) ] )
            #QgsMapLayerRegistry.instance().addMapLayer(polyLayer)
            allFeatures=False
            if not layer.selectedFeatures():
                layer.invertSelection();
                allFeatures=True
            #save original target area
            origTargetArea=targetArea
            # Loop though all the selected features
            for feature in layer.selectedFeatures():
                geom = feature.geometry()
                if self.debug: print "Starting Number of original geoms: ",str(len(geom.asGeometryCollection()))
                if self.debug: print "Starting Number of part to split into: ",str(geom.area()/targetArea)
                div=round(geom.area()/origTargetArea)
                if div<1:
                    div=1
                if splitEven:
                    targetArea=geom.area()/div
                    if self.debug: print "Spliteven selected. modifying target area to:", targetArea
                if div>1:
                    granularity=round(granulFactor*geom.area()/targetArea)
                    if self.debug: print "Granularity: ",granularity
                    #Figure out direction to start with from cutting method
                    #If alternating, start horizontally
                    if method=="a":
                        firstDirection="h"
                    else:
                        firstDirection=method
                    self.alternatingSlice(geom,polyLayer,targetArea,granularity,firstDirection,method)
                else:
                    self.addGeomToLayer(geom,polyLayer)
            polyLayer.updateExtents()
            #if self.debug: print recurs
            QgsMapLayerRegistry.instance().addMapLayer(polyLayer)
            if allFeatures:
                layer.invertSelection();

    def splitSelectedByNumber(self,layerName, div, method="h", tilt=90, checkNewShape = False, shpPath = "result", checkExitingShape = False, checkResultToMap = True):
        global recurs
        recurs=0;
        if layerName == "" :
            QMessageBox.warning(iface.mainWindow(), "error", "At least a polygon layer must be selected.")
            return
        maplist = QgsMapLayerRegistry.instance().mapLayersByName(layerName)
        layer = maplist[0]
        if layer:
            #Gets layer CRS for new layer
            crs=layer.crs().description()
            if self.debug: print "Starting, Layer crs: " + crs
            # Create a new memory layer and add an area attribute
            
            polName = "%s_%s_%i" % (layerName, method, div)
            polyLayer = QgsVectorLayer("MultiPolygon?crs="+crs, polName, "memory")
            polyLayer.dataProvider().addAttributes( [ QgsField("strataArea", QVariant.Double) ] )
            #QgsMapLayerRegistry.instance().addMapLayer(polyLayer)
            allFeatures=False
            if not layer.selectedFeatures():
                layer.invertSelection();
                allFeatures=True
            #save original target area
#             origTargetArea=targetArea
            # Loop though all the selected features
            progressMessageBar = iface.messageBar().createMessage("splitting...")
            self.progress = QProgressBar()
            self.progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            self.progress.setMaximum(div * layer.selectedFeatureCount())
            progressMessageBar.layout().addWidget(self.progress)
            iface.messageBar().pushWidget(progressMessageBar, iface.messageBar().INFO)
            self.progress.setValue(1)
            
            for feature in layer.selectedFeatures():
                geom = feature.geometry()
                targetArea=geom.area()/div
                granularity = div * 2
                if self.debug: print "Starting Number of original geoms: ",str(len(geom.asGeometryCollection()))
                if self.debug: print "Starting Number of part to split into: ",str(geom.area()/div)
#                 div=round(geom.area()/origTargetArea)
                if div<1:
                    div=1
                if div>1:
#                     granularity=round(granulFactor*geom.area()/targetArea)
#                     if self.debug: print "Granularity: ",granularity
                    #Figure out direction to start with from cutting method
                    #If alternating, start horizontally
                    if tilt == 0 or tilt == 90:
                        self.alternatingSlice(geom,polyLayer,targetArea,granularity,method,method)
                    else:
                        if method == "h":
                            self.alternatingSliceTilt(geom, polyLayer, targetArea, granularity, tilt + 90)
                        else:
                            self.alternatingSliceTilt(geom, polyLayer, targetArea, granularity, tilt)
                else:
                    self.addGeomToLayer(geom,polyLayer)
            polyLayer.commitChanges()
            self.progress.setValue(div * layer.selectedFeatureCount())

            polyLayer.updateExtents()
            #if self.debug: print recurs
            if checkResultToMap:                           
                QgsMapLayerRegistry.instance().addMapLayer(polyLayer)
            if checkNewShape:
                QgsVectorFileWriter.writeAsVectorFormat(polyLayer, shpPath, 'utf-8', polyLayer.crs())
            if checkExitingShape:                                
                polyLayer.selectAll ()                
                layer.dataProvider().addFeatures(polyLayer.selectedFeatures())
                layer.updateExtents()
                layer.selectAll()
                layer.invertSelection()
            if allFeatures:
                layer.invertSelection()
            iface.messageBar().hide()


    def alternatingSlice(self,geom,polyLayer,targetArea,granularity,direction,method):
        """
        Slice a poly in alternating directions
        """
        global recurs
        recurs+=1
        if self.debug: print "******************************"
        if self.debug: print "Slicing, No of part: ",str(recurs)
        if self.debug: print "Slicing, Granularity remaining: ", str(granularity)
        if self.debug: print "Slicing, direction: ", direction
        bbox=[geom.boundingBox().xMinimum(),geom.boundingBox().yMinimum(),geom.boundingBox().xMaximum(),geom.boundingBox().yMaximum()]
        if direction=="h":
            step=(bbox[2]-bbox[0])/granularity
            pointer=bbox[0]
        else:
            step=(bbox[3]-bbox[1])/granularity
            pointer=bbox[1]
        totalArea=0
        slices=0
        #save the original geom
        tempGeom=QgsGeometry(geom)
        #start slicing until targetArea is reached
        stepMode = "course"
        stepDirection = 1 # +1 foreword, -1 backword
        fineStep = step
        while abs(totalArea - targetArea) / targetArea > 0.005:
            if self.debug:
                print stepMode + ":" + str(stepDirection)
            pointer+=fineStep * stepDirection
            if direction=="h":
                startPt=QgsPoint(pointer,bbox[1])
                endPt=QgsPoint(pointer,bbox[3])
                
                if stepDirection == 1:
                    (multiGeom, tempGeom)=self.cutPoly(tempGeom,startPt,endPt)
                else:
                    (tempGeom, multiGeom)=self.cutPoly(tempGeom,startPt,endPt)
            else:
                startPt=QgsPoint(bbox[0],pointer)
                endPt=QgsPoint(bbox[2],pointer)
                if stepDirection == 1:
                    (tempGeom, multiGeom)=self.cutPoly(tempGeom,startPt,endPt)
                else:
                    (multiGeom, tempGeom)=self.cutPoly(tempGeom,startPt,endPt)
            if multiGeom!=None:
                totalArea += stepDirection * multiGeom.area();
            
            if totalArea > targetArea:
                stepMode = "fine"
                
            if stepMode == "fine":
                if totalArea > targetArea:
                    if stepDirection != -1:
                        fineStep = fineStep / 2
                        tempGeom = multiGeom
                    stepDirection = -1
                else:
                    if stepDirection != 1:
                        fineStep = fineStep / 2
                        tempGeom = multiGeom
                    stepDirection = 1
                            
            slices+=1
        if self.debug: print "Slicing, Slices: ", str(slices)
        #do the real cutting when reached targetArea and add "left" feature to layer
        if self.debug: print "Cutting with line, Cutline:", startPt,",",endPt
        if direction=="h":
            (multiGeom, leftgeom)=self.cutPoly(geom,startPt,endPt,True)
            if multiGeom:
                if self.debug: print "After split, Parts to the left:",str(len(multiGeom.asGeometryCollection()))
            if leftgeom:
                if self.debug: print "After split, Parts to the right:",str(len(geom.asGeometryCollection()))
        else:
            (leftgeom,multiGeom)=self.cutPoly(geom,startPt,endPt,True)
            if leftgeom:
                if self.debug: print "After split, Parts above:",str(len(geom.asGeometryCollection()))
            if multiGeom:
                if self.debug: print "After split, Parts under:",str(len(multiGeom.asGeometryCollection()))
        #self.addGeomToLayer(QgsGeometry.fromPolyline([startPt,endPt]),lineLayer)
        
        if leftgeom:
            if leftgeom.area()>targetArea:
                if (method=="v") or ((method=="a") and (direction=="h")):
                    self.alternatingSlice(leftgeom,polyLayer,targetArea,granularity,"v",method)
                else:
                    self.alternatingSlice(leftgeom,polyLayer,targetArea,granularity,"h",method)
            elif leftgeom.area() < targetArea / 2:
                multiGeom = geom
            else:
                self.addGeomToLayer(leftgeom,polyLayer)
        self.addGeomToLayer(multiGeom,polyLayer)

    def alternatingSliceTilt(self,geom,polyLayer,targetArea,granularity,tilt):
        """
        Slice a poly in alternating directions
        """
        global recurs
        recurs+=1
        if self.debug: print "******************************"
        if self.debug: print "Slicing, No of part: ",str(recurs)
        if self.debug: print "Slicing, Granularity remaining: ", str(granularity)
        if self.debug: print "Slicing, direction: ", tilt
        bbox=[geom.boundingBox().xMinimum(),geom.boundingBox().yMinimum(),geom.boundingBox().xMaximum(),geom.boundingBox().yMaximum()]
        if tilt > 90 :
            tilt_new = 180 - tilt
            if bbox[2]-bbox[0] > bbox[3]-bbox[1]:
                granulY=(bbox[3]-bbox[1])/granularity
                stepY = granulY            
                stepX = math.tan(math.radians(tilt_new)) * granulY
            else:
                granulX=(bbox[2]-bbox[0])/granularity
                stepX = granulX
                stepY =  granulX / math.tan(math.radians(tilt_new))
        else:
            if bbox[2]-bbox[0] > bbox[3]-bbox[1]:
                granulY=(bbox[3]-bbox[1])/granularity
                stepY = -1 * granulY            
                stepX = math.tan(math.radians(tilt)) * granulY
            else:
                granulX=(bbox[2]-bbox[0])/granularity
                stepX = granulX
                stepY =  -1 * granulX / math.tan(math.radians(tilt))
            
#         granulX=(bbox[2]-bbox[0])/granularity
#         granulY=(bbox[3]-bbox[1])/granularity
        baseX = bbox[0]
        pointerX = bbox[0]
        if 180 > tilt > 90:
#             stepX = granulX / abs(math.cos(math.radians(tilt)))
#             stepY = granulY / abs(math.sin(math.radians(tilt)))
            pointerY=bbox[1]
            baseY = bbox[1]
        elif 90 > tilt > 0:
#             stepX = granulX / abs(math.cos(math.radians(tilt)))
#             stepY = -1 * granulY / abs(math.sin(math.radians(tilt)))
            pointerY=bbox[3]
            baseY = bbox[3]
        elif tilt == 90 or tilt == 0 or tilt >= 180:
            QMessageBox.warning(iface.mainWindow(), "Warning", "The value of tilt is incorrect!\n It must be in range 0-180.\ntilt:%i" % tilt)
        totalArea=0
        slices=0
        #save the original geom
        tempGeom=QgsGeometry(geom)
        #start slicing until targetArea is reached
        stepMode = "course"
        stepDirection = 1 # +1 foreword, -1 backword
        fineStepX = stepX
        fineStepY = stepY
        while abs(totalArea - targetArea) / targetArea > 0.005:
            
            if self.debug: print stepMode + ":" + str(stepDirection)
            if self.debug: print "fineStepX" + ":" + str(fineStepX)
            if self.debug: print "fineStepY" + ":" + str(fineStepY)
            if self.debug: print "baseX" + ":" + str(baseX)
            if self.debug: print "baseY" + ":" + str(baseY)
            
            pointerX += fineStepX * stepDirection
            pointerY += fineStepY * stepDirection
            
            if self.debug: print "pointerX" + ":" + str(pointerX)
            if self.debug: print "pointerY" + ":" + str(pointerY)
            
            startPt=QgsPoint(pointerX,baseY)
            endPt=QgsPoint(baseX,pointerY)
            
            if tilt < 90:
                if stepDirection == 1:
                    (tempGeom, multiGeom)=self.cutPoly(tempGeom,startPt,endPt)
                else:
                    (multiGeom, tempGeom)=self.cutPoly(tempGeom,startPt,endPt)
            else:
                if stepDirection == 1:
                    (multiGeom, tempGeom)=self.cutPoly(tempGeom,startPt,endPt)
                else:
                    (tempGeom, multiGeom)=self.cutPoly(tempGeom,startPt,endPt)
            if multiGeom!=None:
                totalArea += stepDirection * multiGeom.area();
            
            if totalArea > targetArea:
                stepMode = "fine"
                
            if stepMode == "fine":
                if totalArea > targetArea:
                    if stepDirection != -1:
                        fineStepX = fineStepX / 2
                        fineStepY = fineStepY / 2
                        tempGeom = multiGeom
                    stepDirection = -1
                else:
                    if stepDirection != 1:
                        fineStepX = fineStepX / 2
                        fineStepY = fineStepY / 2
                        tempGeom = multiGeom
                    stepDirection = 1
            if self.debug: print "totalArea" + ":" + str(totalArea)
            if self.debug: print "targetArea" + ":" + str(targetArea)
            slices+=1
            
        self.progress.setValue(recurs + 1)

        if self.debug: print "Slicing, Slices: ", str(slices)
        #do the real cutting when reached targetArea and add "left" feature to layer
        if self.debug: print "Cutting with line, Cutline:", startPt,",",endPt
        
        if tilt < 90:
            (leftgeom, multiGeom)=self.cutPoly(geom,startPt,endPt,True)
        else:
            (multiGeom, leftgeom)=self.cutPoly(geom,startPt,endPt,True)
            
        if multiGeom:
            if self.debug: print "After split, Parts to the left:",str(len(multiGeom.asGeometryCollection()))
        if leftgeom:
            if self.debug: print "After split, Parts to the right:",str(len(geom.asGeometryCollection()))
        
        if leftgeom:
            if leftgeom.area()>targetArea:
                self.alternatingSliceTilt(leftgeom,polyLayer,targetArea,granularity,tilt)
            elif leftgeom.area() < targetArea / 2:
                multiGeom = geom
            else:
                self.addGeomToLayer(leftgeom,polyLayer)
        self.addGeomToLayer(multiGeom,polyLayer)

    def cutPoly(self,geom,startPt,endPt,debug=False):
        """
        Cut a geometry by a 2 point line
        return geoms left of line and right of line
        """
        #if we have disjoint Multi geometry as geom to split we need to iterate over its parts
        splittedGeoms=[]
        leftFragments=[]
        rightFragments=[]
        #if self.debug: print "Number of geoms when slicing: ",str(len(geom.asGeometryCollection()))
        for geomPart in geom.asGeometryCollection():
            #split the actual part by cut line defined by startPt,endPt
            (res,splittedGeomsPart,topo)=geomPart.splitGeometry([startPt,endPt],False)
            splittedGeoms+=splittedGeomsPart
            #Add the remaining geomPart to the rightFragments or letfFragments
            #depending on distance
            d=self.signedDistCentroidFromLine(geomPart,startPt,endPt)
            if debug==True:
                if self.debug: print "geomPart:", d
            if d>0:
                rightFragments.append(geomPart)
            else:
                leftFragments.append(geomPart)
            #if self.debug: print j,splittedGeoms

        for fragment in splittedGeoms:
            """
            calculate signed distance of centroid of fragment and the splitline
            if signed distance is below zero, the point is to the left of the line
            if above zero the point is to the right of the line
            """
            d=self.signedDistCentroidFromLine(fragment,startPt,endPt)
            if debug==True:
                if self.debug: print "fragment:", d

            if d>0:
                rightFragments.append(fragment)
            else:
                leftFragments.append(fragment)

        #if self.debug: print "Left frags:",len(leftFragments),"Right frags:",len(rightFragments)
        leftGeom=self.buildMultiPolygon(leftFragments)
        rightGeom=self.buildMultiPolygon(rightFragments)
        return leftGeom,rightGeom

    def buildMultiPolygon(self,polygonList):
        """
        Build multi polygon feature from a list of polygons
        """
        geomlist=[]
        for geom in polygonList:
            # Cut 'MULTIPOLYGON(*) if we got one'
            if geom.exportToWkt()[:12]=="MULTIPOLYGON":
                geomWkt=geom.exportToWkt()[13:len(geom.exportToWkt())-1]
            else:
                # Cut 'POLYGON' if we got one
                geomWkt=geom.exportToWkt()[7:]
            geomlist.append(str(geomWkt))
        multiGeomWKT="MULTIPOLYGON("
        multiGeomWKT +=",".join(geomlist)
        multiGeomWKT+=")"
        #if self.debug: print multiGeomWKT
        multiGeom=QgsGeometry.fromWkt(multiGeomWKT)
        return multiGeom

    def addGeomToLayer(self,geom,layer):
        """
        Add a geometry to a layer as a new feature
        No attributes are set
        """
        fet = QgsFeature()
        fet.setGeometry(geom)
        area=geom.area()#/1000000
        #QMessageBox.warning(iface.mainWindow(), "test", str(area))
        if self.debug: print "Area of geom added to layer:", str(area)
        fet.setAttributes( [area] )
        layer.dataProvider().addFeatures([fet])
        layer.updateExtents()

    def signedDistCentroidFromLine(self,geom,startPt,endPt):
        #calculate signed distance of centroid of fragment and the splitline
        v1=endPt[0]-startPt[0]
        v2=endPt[1]-startPt[1]
        A=v2
        B=-v1
        C=-v2*startPt[0]+v1*startPt[1]
        centr=geom.centroid().boundingBox()
        return (A*centr.xMinimum()+B*centr.yMinimum()+C)/math.sqrt(A**2+B**2)

#run_script(iface)


