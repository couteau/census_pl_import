""" Import dialog

        begin                : 2022-08-18
        copyright            : (C) 2022 by Cryptodira
        email                : stuart@cryptodira.org
        git sha              : $Format:%H$

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful, but   *
 *   WITHOUT ANY WARRANTY; without even the implied warranty of            *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          *
 *   GNU General Public License for more details. You should have          *
 *   received a copy of the GNU General Public License along with this     *
 *   program. If not, see <http://www.gnu.org/licenses/>.                  *
 *                                                                         *
 ***************************************************************************/
"""
import pathlib
import re
from typing import Optional, Union
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QDialog, QWidget, QDialogButtonBox
from qgis.core import QgsVectorLayer

from .dlg_import_base import Ui_dlgRDHImport
from ..import_utils import GeographyType


class DlgImport(Ui_dlgRDHImport, QDialog):
    def __init__(self, parent: Optional[QWidget] = None, flags: Union[Qt.WindowFlags, Qt.WindowType] = Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.setupUi(self)

        self.fwPLFile.fileChanged.connect(self.update_pl_file)
        self.fwACSFile.fileChanged.connect(self.update_acs_file)
        self.fwOutput.fileChanged.connect(self.update_buttons)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

    def update_buttons(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
            bool(self.fwOutput.filePath()) and
            bool(self.fwPLFile.filePath())
        )

    def geography(self, path=None):
        geo_types = {
            'b': GeographyType.BLOCK,
            'vtd': GeographyType.VTD,
            'cnty': GeographyType.COUNTY,
            'bg': GeographyType.BLKGRP,
            't': GeographyType.TRACT
        }
        if path is None:
            path = self.fwPLFile.filePath()
        p = pathlib.Path(path).stem.split('_')[-1]
        if p in geo_types:
            return geo_types[p]
        return -1

    def state(self, path=None):
        if path is None:
            path = self.fwPLFile.filePath()
        return pathlib.Path(path).stem.split('_')[0]

    def year(self):
        return(pathlib.Path(self.fwPLFile.filePath()).stem.split('_')[1][:2])

    def check_files_match(self):
        self.lbStatus.setText('')
        pl_file = self.fwPLFile.filePath()
        acs_file = self.fwACSFile.filePath()
        if pl_file and acs_file:
            pl = QgsVectorLayer(pl_file)
            acs = QgsVectorLayer(acs_file)
            if pl.isValid() and acs.isValid():
                if self.state(pl_file) != self.state(acs_file):
                    self.lbStatus.setText(self.tr('PL and ACS files come from different states'))
                elif self.geography(pl_file) != self.geography(acs_file):
                    self.lbStatus.setText(self.tr('PL and ACS files are at different levels of census geography'))
                elif pl.featureCount() != acs.featureCount():
                    self.lbStatus.setText(self.tr('PL and ACS files have different numbers of features'))

    def update_pl_file(self, path):
        def layerName(t: GeographyType):
            if t == GeographyType.BLOCK:
                return 'block'
            if t == GeographyType.VTD:
                return 'vtd'
            if t == GeographyType.COUNTY:
                return 'county'
            if t == GeographyType.BLKGRP:
                return 'blkgrp'
            if t == GeographyType.TRACT:
                return 'tract'

            return 'rdh_pl_data'

        self.edTableName.setText(layerName(self.geography()))
        self.cbAppend.setEnabled(pathlib.Path(path).resolve().exists())
        self.cbAppend.setChecked(pathlib.Path(path).resolve().exists())
        self.check_files_match()
        self.update_decennial_year()
        self.update_buttons()

    def update_acs_file(self):
        self.check_files_match()
        self.update_acs_year()

    def update_decennial_year(self):
        file = self.fwPLFile.filePath()
        if match := re.search(r'pl((!:19|20)\d{2})', file):
            self.spDecennialYear.setClearValue(int(match[1]))
            self.spDecennialYear.setValue(int(match[1]))

    def update_acs_year(self):
        file = self.fwACSFile.filePath()
        if match := re.search(r'cvap_((!:19|20)\d{2})', file):
            self.spACSYear.setClearValue(int(match[1]))
            self.spACSYear.setValue(int(match[1]))
