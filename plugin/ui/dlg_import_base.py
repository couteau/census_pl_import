# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/stuart/Source/rdh_import/ui/dlg_import.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dlgRDHImport(object):
    def setupUi(self, dlgRDHImport):
        dlgRDHImport.setObjectName("dlgRDHImport")
        dlgRDHImport.resize(465, 326)
        self.gridLayout = QtWidgets.QGridLayout(dlgRDHImport)
        self.gridLayout.setObjectName("gridLayout")
        self.lbPLFile = QtWidgets.QLabel(dlgRDHImport)
        self.lbPLFile.setObjectName("lbPLFile")
        self.gridLayout.addWidget(self.lbPLFile, 0, 0, 1, 1)
        self.fwPLFile = gui.QgsFileWidget(dlgRDHImport)
        self.fwPLFile.setObjectName("fwPLFile")
        self.gridLayout.addWidget(self.fwPLFile, 0, 1, 1, 1)
        self.lbDecennialYear = QtWidgets.QLabel(dlgRDHImport)
        self.lbDecennialYear.setObjectName("lbDecennialYear")
        self.gridLayout.addWidget(self.lbDecennialYear, 1, 0, 1, 1)
        self.spDecennialYear = gui.QgsSpinBox(dlgRDHImport)
        self.spDecennialYear.setMinimum(1970)
        self.spDecennialYear.setMaximum(2050)
        self.spDecennialYear.setSingleStep(10)
        self.spDecennialYear.setProperty("value", 2020)
        self.spDecennialYear.setObjectName("spDecennialYear")
        self.gridLayout.addWidget(self.spDecennialYear, 1, 1, 1, 1)
        self.lbACSFile = QtWidgets.QLabel(dlgRDHImport)
        self.lbACSFile.setObjectName("lbACSFile")
        self.gridLayout.addWidget(self.lbACSFile, 2, 0, 1, 1)
        self.fwACSFile = gui.QgsFileWidget(dlgRDHImport)
        self.fwACSFile.setObjectName("fwACSFile")
        self.gridLayout.addWidget(self.fwACSFile, 2, 1, 1, 1)
        self.lbACSYear = QtWidgets.QLabel(dlgRDHImport)
        self.lbACSYear.setObjectName("lbACSYear")
        self.gridLayout.addWidget(self.lbACSYear, 3, 0, 1, 1)
        self.spACSYear = gui.QgsSpinBox(dlgRDHImport)
        self.spACSYear.setMinimum(1980)
        self.spACSYear.setMaximum(2050)
        self.spACSYear.setSingleStep(1)
        self.spACSYear.setProperty("value", 2020)
        self.spACSYear.setObjectName("spACSYear")
        self.gridLayout.addWidget(self.spACSYear, 3, 1, 1, 1)
        self.lbOutput = QtWidgets.QLabel(dlgRDHImport)
        self.lbOutput.setObjectName("lbOutput")
        self.gridLayout.addWidget(self.lbOutput, 4, 0, 1, 1)
        self.fwOutput = gui.QgsFileWidget(dlgRDHImport)
        self.fwOutput.setStorageMode(gui.QgsFileWidget.SaveFile)
        self.fwOutput.setObjectName("fwOutput")
        self.gridLayout.addWidget(self.fwOutput, 4, 1, 1, 1)
        self.lbTableName = QtWidgets.QLabel(dlgRDHImport)
        self.lbTableName.setObjectName("lbTableName")
        self.gridLayout.addWidget(self.lbTableName, 5, 0, 1, 1)
        self.edTableName = QtWidgets.QLineEdit(dlgRDHImport)
        self.edTableName.setObjectName("edTableName")
        self.gridLayout.addWidget(self.edTableName, 5, 1, 1, 1)
        self.cbKeepRDHdata = QtWidgets.QCheckBox(dlgRDHImport)
        self.cbKeepRDHdata.setObjectName("cbKeepRDHdata")
        self.gridLayout.addWidget(self.cbKeepRDHdata, 6, 0, 1, 3)
        self.cbAddToProject = QtWidgets.QCheckBox(dlgRDHImport)
        self.cbAddToProject.setChecked(True)
        self.cbAddToProject.setObjectName("cbAddToProject")
        self.gridLayout.addWidget(self.cbAddToProject, 7, 0, 1, 2)
        self.lbStatus = QtWidgets.QLabel(dlgRDHImport)
        self.lbStatus.setStyleSheet("QLabel {\n"
"    color: red;\n"
"}")
        self.lbStatus.setText("")
        self.lbStatus.setObjectName("lbStatus")
        self.gridLayout.addWidget(self.lbStatus, 8, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlgRDHImport)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 11, 0, 1, 2)

        self.retranslateUi(dlgRDHImport)
        self.buttonBox.accepted.connect(dlgRDHImport.accept)
        self.buttonBox.rejected.connect(dlgRDHImport.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgRDHImport)

    def retranslateUi(self, dlgRDHImport):
        _translate = QtCore.QCoreApplication.translate
        dlgRDHImport.setWindowTitle(_translate("dlgRDHImport", "Import RDH PL File"))
        self.lbPLFile.setText(_translate("dlgRDHImport", "Path to RDH PL file"))
        self.fwPLFile.setDialogTitle(_translate("dlgRDHImport", "Select PL data file"))
        self.fwPLFile.setFilter(_translate("dlgRDHImport", "*.shp"))
        self.lbDecennialYear.setText(_translate("dlgRDHImport", "Decennial Census Year"))
        self.lbACSFile.setText(_translate("dlgRDHImport", "Path to RDH ACS file"))
        self.fwACSFile.setDialogTitle(_translate("dlgRDHImport", "Select ACS data file"))
        self.fwACSFile.setFilter(_translate("dlgRDHImport", "*.shp; *.csv"))
        self.lbACSYear.setText(_translate("dlgRDHImport", "ACS Year"))
        self.lbOutput.setText(_translate("dlgRDHImport", "Destination GeoPackage"))
        self.fwOutput.setDialogTitle(_translate("dlgRDHImport", "Save GeoPackage"))
        self.fwOutput.setFilter(_translate("dlgRDHImport", "*.gpkg"))
        self.lbTableName.setText(_translate("dlgRDHImport", "Destination Table Name"))
        self.cbKeepRDHdata.setText(_translate("dlgRDHImport", "Keep raw data tables"))
        self.cbAddToProject.setText(_translate("dlgRDHImport", "Add Imported Layer to Project"))
from qgis import gui