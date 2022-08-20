""" RDH Import - A QGIS plugin for importing U.S. Census data
    from Redistrictin Data Hub PL Shapefiles into GeoPackage

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
from qgis.PyQt.QtCore import QCoreApplication, QSettings, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QDialog, QToolBar
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsTask,
    QgsTaskWrapper,
    QgsVectorLayer,
    QgsVectorFileWriter,
    QgsVectorFileWriterTask
)
from qgis.gui import QgisInterface

from .ui import DlgImport
from .import_utils import GeographyType, spatialite_connect, createGeoPackage
from .sql import create_sql, select_sql
from .resources import *  # pylint: disable=wildcard-import,unused-wildcard-import


class RDHImport:

    def __init__(self, iface: QgisInterface):
        self.name = self.__class__.__name__
        self.iface = iface

        # initialize locale
        pluginDir = pathlib.Path(__file__).parent
        locale = QSettings().value('locale/userLocale')[0:2]
        localePath = pluginDir / 'i18n' / f'{self.name}_{locale}.qm'

        if localePath.exists():
            self.translator = QTranslator()
            self.translator.load(str(localePath))
            QCoreApplication.installTranslator(self.translator)

        self.action: QAction = None
        self.menuName = self.tr('&RDH Import')
        self.toolbar: QToolBar = None

    @staticmethod
    def tr(message):
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('redistricting', message)

    def initGui(self):
        self.toolbar: QToolBar = self.iface.addToolBar(self.name)
        self.toolbar.setObjectName(self.name)

        icon = QIcon(':/plugins/rdh_import/icon.png')
        self.action = QAction(icon, self.tr('RDH Import'), self.iface.mainWindow())
        self.action.triggered.connect(self.onImportAction)
        self.toolbar.addAction(self.action)
        self.iface.addPluginToVectorMenu(
            self.menuName,
            self.action)

    def unload(self):
        self.iface.removePluginVectorMenu(self.menuName, self.action)
        self.iface.removeToolBarIcon(self.action)
        del self.toolbar

    @staticmethod
    def createLayerFromQuery(
            task: QgsTaskWrapper,
            out_path,
            table_name,
            geography,
            pl_path,
            pl_year,
            acs_path,
            acs_year,
            keep):

        try:
            with spatialite_connect(out_path) as db:
                pl_shortyear = str(pl_year)[2:]
                geoid_field = f'geoid{pl_shortyear}'
                src_layer = pathlib.Path(pl_path).stem
                if acs_path and acs_year:
                    cvap_layer = pathlib.Path(acs_path).stem

                db.execute(f'CREATE INDEX {src_layer}_{geoid_field} ON {src_layer} ({geoid_field})')
                if acs_path and acs_year:
                    db.execute(f'CREATE INDEX {cvap_layer}_{geoid_field} ON {cvap_layer} ({geoid_field})')

                sql = create_sql(geography, table_name, geoid_field, pl_year, bool(acs_path), acs_year)
                db.execute(sql)

                crs = db.execute(
                    f'SELECT srs_id FROM gpkg_geometry_columns WHERE table_name = \'{src_layer}\'').fetchone()[0]
                sql = f'SELECT gpkgAddGeometryColumn(\'{table_name}\', \'geom\', \'MULTIPOLYGON\', 0, 0, {crs})'
                db.execute(sql)

                sql = select_sql(
                    geography,
                    geoid_field,
                    src_layer,
                    pl_year,
                    pathlib.Path(acs_path).stem,
                    acs_year
                )

                sql = f'INSERT INTO {table_name} {sql}'
                db.execute(sql)

                if not keep:
                    db.execute(f'DROP TABLE {src_layer}')
                    if acs_path and acs_year:
                        db.execute(f'DROP TABLE {cvap_layer}')
        except Exception as e:  # pylint: disable=broad-except
            task.exception = e
            return False

        return True

    def importRDHData(self,  # pylint: disable=too-many-arguments
                      out_path: str, out_layer: str,
                      pl_path: str, pl_year: int = 0,
                      acs_path: str = '', acs_year: int = 0,
                      geography: GeographyType = GeographyType.BLOCK,
                      keep: bool = False,
                      overwrite: bool = True):

        if overwrite or not pathlib.Path(out_path).resolve().exists():
            success, message = createGeoPackage(out_path)
            if not success:
                self.iface.messageBar().pushCritical('Error', str(message))
                return None

        query_task: QgsTaskWrapper = QgsTask.fromFunction(
            'Import RDH shapefile',
            RDHImport.createLayerFromQuery,
            out_path,
            out_layer,
            geography,
            pl_path,
            pl_year,
            acs_path,
            acs_year,
            keep
        )

        pl_layer = QgsVectorLayer(pl_path, 'rdh_import_pl', 'ogr')
        QgsProject.instance().addMapLayer(pl_layer, False)
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
        options.driverName = 'GPKG'
        options.layerName = pathlib.Path(pl_path).stem
        import_pl_task = QgsVectorFileWriterTask(pl_layer, out_path, options)
        query_task.addSubTask(import_pl_task, subTaskDependency=QgsTask.ParentDependsOnSubTask)

        if acs_path and acs_year:
            acs_layer = QgsVectorLayer(acs_path, 'rdh_import_acs', 'ogr')
            QgsProject.instance().addMapLayer(acs_layer, False)
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
            options.driverName = 'GPKG'
            options.layerName = pathlib.Path(acs_path).stem
            import_acs_task = QgsVectorFileWriterTask(acs_layer, out_path, options)
            query_task.addSubTask(import_acs_task, subTaskDependency=QgsTask.ParentDependsOnSubTask)

        QgsApplication.taskManager().addTask(query_task)
        return query_task

    def onImportAction(self):
        def addToProject(exception):
            if not exception:
                layer = QgsVectorLayer(
                    f'{out_file}|layername={table}', table, 'ogr'
                )
                if len(QgsProject.instance().mapLayers()) == 0:
                    QgsProject.instance().setCrs(layer.crs())
                QgsProject.instance().addMapLayer(layer)
            else:
                self.iface.messageBar().pushCritical('Error', str(task.exception))

        dlg = DlgImport(self.iface.mainWindow())
        if dlg.exec_() == QDialog.Accepted:
            pl_file = dlg.fwPLFile.filePath()
            acs_file = dlg.fwACSFile.filePath()
            out_file = dlg.fwOutput.filePath()
            table = dlg.edTableName.text()
            pl_year = dlg.spDecennialYear.value()
            acs_year = dlg.spACSYear.value()
            task = self.importRDHData(
                out_file, table,
                pl_file, pl_year,
                acs_file, acs_year,
                dlg.geography(),
                dlg.cbKeepRDHdata.isChecked()
            )
            if task and dlg.cbAddToProject.isChecked():
                task.on_finished = addToProject
