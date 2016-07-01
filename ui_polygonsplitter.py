# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_polygonsplitter.ui'
#
# Created: Wed Oct 15 15:49:22 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_polygonsplitter(object):
    def setupUi(self, polygonsplitter):
        polygonsplitter.setObjectName(_fromUtf8("polygonsplitter"))
        polygonsplitter.setWindowModality(QtCore.Qt.ApplicationModal)
        polygonsplitter.resize(469, 446)
        self.buttonBox = QtGui.QDialogButtonBox(polygonsplitter)
        self.buttonBox.setGeometry(QtCore.QRect(280, 400, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(polygonsplitter)
        self.label.setGeometry(QtCore.QRect(40, 20, 381, 41))
        self.label.setToolTip(_fromUtf8(""))
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox_2 = QtGui.QGroupBox(polygonsplitter)
        self.groupBox_2.setGeometry(QtCore.QRect(220, 130, 191, 141))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalCut = QtGui.QRadioButton(self.groupBox_2)
        self.verticalCut.setGeometry(QtCore.QRect(20, 20, 121, 17))
        self.verticalCut.setObjectName(_fromUtf8("verticalCut"))
        self.horizontalCut = QtGui.QRadioButton(self.groupBox_2)
        self.horizontalCut.setGeometry(QtCore.QRect(20, 50, 131, 17))
        self.horizontalCut.setObjectName(_fromUtf8("horizontalCut"))
        self.alternatingCut = QtGui.QRadioButton(self.groupBox_2)
        self.alternatingCut.setGeometry(QtCore.QRect(20, 80, 161, 17))
        self.alternatingCut.setChecked(True)
        self.alternatingCut.setObjectName(_fromUtf8("alternatingCut"))
        self.tiltFactor = QtGui.QSpinBox(self.groupBox_2)
        self.tiltFactor.setGeometry(QtCore.QRect(100, 110, 51, 22))
        self.tiltFactor.setMinimum(0)
        self.tiltFactor.setMaximum(90)
        self.tiltFactor.setObjectName(_fromUtf8("tiltFactor"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 61, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox = QtGui.QGroupBox(polygonsplitter)
        self.groupBox.setGeometry(QtCore.QRect(40, 160, 121, 71))
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.divisionsNum = QtGui.QDoubleSpinBox(self.groupBox)
        self.divisionsNum.setGeometry(QtCore.QRect(30, 30, 51, 22))
        self.divisionsNum.setDecimals(0)
        self.divisionsNum.setMinimum(0.0)
        self.divisionsNum.setMaximum(1e+15)
        self.divisionsNum.setProperty("value", 2.0)
        self.divisionsNum.setObjectName(_fromUtf8("divisionsNum"))
        self.checkNewShape = QtGui.QCheckBox(polygonsplitter)
        self.checkNewShape.setGeometry(QtCore.QRect(30, 310, 131, 17))
        self.checkNewShape.setObjectName(_fromUtf8("checkNewShape"))
        self.checkAddExisting = QtGui.QCheckBox(polygonsplitter)
        self.checkAddExisting.setGeometry(QtCore.QRect(30, 340, 151, 17))
        self.checkAddExisting.setObjectName(_fromUtf8("checkAddExisting"))
        self.checkResultMap = QtGui.QCheckBox(polygonsplitter)
        self.checkResultMap.setGeometry(QtCore.QRect(30, 370, 121, 17))
        self.checkResultMap.setObjectName(_fromUtf8("checkResultMap"))
        self.checkResultMap.setChecked(True)
        self.editShapeFile = QtGui.QLineEdit(polygonsplitter)
        self.editShapeFile.setGeometry(QtCore.QRect(160, 307, 231, 23))
        self.editShapeFile.setObjectName(_fromUtf8("editShapeFile"))
        self.btnBrowse = QtGui.QPushButton(polygonsplitter)
        self.btnBrowse.setGeometry(QtCore.QRect(396, 307, 61, 23))
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.comboLayers = QtGui.QComboBox(polygonsplitter)
        self.comboLayers.setGeometry(QtCore.QRect(40, 70, 171, 22))
        self.comboLayers.setObjectName(_fromUtf8("comboLayers"))

        self.retranslateUi(polygonsplitter)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), polygonsplitter.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), polygonsplitter.reject)
        QtCore.QMetaObject.connectSlotsByName(polygonsplitter)

    def retranslateUi(self, polygonsplitter):
        polygonsplitter.setWindowTitle(_translate("polygonsplitter", "Split polygons into equal area parts", None))
        self.label.setText(_translate("polygonsplitter", "Please select a layer", None))
        self.groupBox_2.setTitle(_translate("polygonsplitter", "Direction of cut", None))
        self.verticalCut.setText(_translate("polygonsplitter", "Vertical cutting", None))
        self.horizontalCut.setText(_translate("polygonsplitter", "Horizontal cutting", None))
        self.alternatingCut.setText(_translate("polygonsplitter", "Alternating vert/horiz", None))
        self.tiltFactor.setToolTip(_translate("polygonsplitter", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Multiplier of original polygon area / target area to get iteration steps<br />(recommended value is between 5 and10)</span></p></body></html>", None))
        self.label_2.setText(_translate("polygonsplitter", "Tilt(degree)", None))
        self.groupBox.setTitle(_translate("polygonsplitter", "Number of Divisions", None))
        self.divisionsNum.setToolTip(_translate("polygonsplitter", "Target area of polygon parts", None))
        self.checkNewShape.setText(_translate("polygonsplitter", "create new shape file", None))
        self.checkAddExisting.setText(_translate("polygonsplitter", "add to existing shape file", None))
        self.checkResultMap.setText(_translate("polygonsplitter", "add result to map", None))
        self.btnBrowse.setText(_translate("polygonsplitter", "browse", None))

