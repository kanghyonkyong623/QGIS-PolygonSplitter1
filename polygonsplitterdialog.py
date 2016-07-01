# -*- coding: utf-8 -*-
"""
/***************************************************************************
 polygonsplitterDialog
                                 A QGIS plugin
 Split polygons into equal area parts
                             -------------------
        begin                : 2013-03-07
        copyright            : (C) 2013 by ViaMap Ltd.
        email                : info@viamap.hu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.gui import *
from qgis.core import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
# from qgis.utils import*
from ui_polygonsplitter import Ui_polygonsplitter
# create the dialog for zoom to point


class polygonsplitterDialog(QDialog):
    def __init__(self, iface):
        QDialog.__init__(self)
#         self.iface = iface
        # Set up the user interface from Designer.
        self.ui = Ui_polygonsplitter()
        self.ui.setupUi(self)
        self.ui.btnBrowse.clicked.connect(self.browse)
        self.ui.btnBrowse.setEnabled(False)
        self.ui.checkNewShape.clicked.connect(self.checkNewShape)

        layers = iface.mapCanvas().layers()
        for value in layers:
            if value.type() == QgsMapLayer.VectorLayer and value.geometryType() == QGis.Polygon :
                self.ui.comboLayers.addItem(value.name()) 
    

    def browse(self):
        
        file = QFileDialog.getSaveFileName(self, "Save Shape File",QCoreApplication.applicationDirPath (),"Shape files(*.shp )")
        self.ui.editShapeFile.setText(file)
    def checkNewShape(self):
        if self.ui.checkNewShape.isChecked():
            self.ui.btnBrowse.setEnabled(True)
            self.ui.editShapeFile.setEnabled(True)
        else:
            self.ui.btnBrowse.setEnabled(False)
            self.ui.editShapeFile.setEnabled(False)

        
         