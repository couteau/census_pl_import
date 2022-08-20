""" Unit tests for plugin class

        begin                : 2022-08-19
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
import sqlite3
from typing import List
import pytest
from pytest_mock import MockerFixture
from plugin import classFactory
from plugin.rdh_import import RDHImport, GeographyType, QgsApplication, QgsTask, QgsVectorFileWriterTask


class TestPlugin:
    @pytest.fixture
    def plugin(self, qgis_iface, mocker: MockerFixture):
        settings = mocker.patch('plugin.rdh_import.QSettings')
        settings_obj = settings.return_value
        settings_obj.value.return_value = 'en_US'
        qgis_iface.vectorMenu = mocker.MagicMock()
        qgis_iface.addPluginToVectorMenu = mocker.MagicMock()
        qgis_iface.removeDockWidget = mocker.MagicMock()
        qgis_iface.removePluginVectorMenu = mocker.MagicMock()

        return classFactory(qgis_iface)

    @pytest.fixture
    def plugin_with_gui(self, plugin):  # pylint: disable=unused-argument
        plugin.initGui()
        yield plugin
        plugin.unload()

    def test_create_plugin(self, plugin):
        assert plugin is not None

    @pytest.mark.parametrize(('shapefile', 'geo_type', 'table', 'year', 'features'), [
        ('de_pl2020_b.zip', GeographyType.BLOCK, 'block', 2020, 20198),
        ('de_pl2020_vtd.shp', GeographyType.VTD, 'vtd', 2020, 412),
        ('de_pl2020_cnty.shp', GeographyType.COUNTY, 'county', 2020, 3),
        ('de_pl2020_t.shp', GeographyType.TRACT, 'tract', 2020, 262),
        ('de_pl2020_bg.shp', GeographyType.BLKGRP, 'blkgrp', 2020, 706),
    ])
    def test_import_pl_only(self, plugin_with_gui: RDHImport, shapefile, geo_type, table, year, features, datadir: pathlib.Path, mocker: MockerFixture):
        def addTask(task: QgsTask, priority: int = 0):  # pylint: disable=unused-argument
            for t in subtasks:
                res = t.run()
                t.finished(res)

            res = task.run()
            task.finished(res)
            if res:
                task.taskCompleted.emit()
            else:
                task.taskTerminated.emit()
            return 1

        def captureSubTask(task, subTask, dependencies=None, subTaskDependency=0):  # pylint: disable=unused-argument
            subtasks.append(subTask)

        subtasks: List[QgsVectorFileWriterTask] = []
        mocker.patch.object(QgsApplication.taskManager(), 'addTask', addTask)
        mocker.patch('plugin.rdh_import.QgsTaskWrapper.addSubTask', captureSubTask)
        plugin_with_gui.importRDHData(
            str(datadir / 'test_out.gpkg'),
            table,
            str(datadir / shapefile),
            year,
            geography=geo_type
        )
        assert (datadir / 'test_out.gpkg').exists()
        with sqlite3.connect(datadir / 'test_out.gpkg') as db:
            count = db.execute(f'SELECT count(*) from {table}').fetchone()[0]
            assert count == features

    def test_import_block_cvap_csv(self, plugin_with_gui: RDHImport, datadir: pathlib.Path, mocker: MockerFixture):
        def addTask(task: QgsTask, priority: int = 0):  # pylint: disable=unused-argument
            for t in subtasks:
                res = t.run()
                t.finished(res)

            res = task.run()
            task.finished(res)
            if res:
                task.taskCompleted.emit()
            else:
                task.taskTerminated.emit()
            return 1

        def captureSubTask(task, subTask, dependencies=None, subTaskDependency=0):  # pylint: disable=unused-argument
            subtasks.append(subTask)

        subtasks: List[QgsVectorFileWriterTask] = []
        mocker.patch.object(QgsApplication.taskManager(), 'addTask', addTask)
        mocker.patch('plugin.rdh_import.QgsTaskWrapper.addSubTask', captureSubTask)
        plugin_with_gui.importRDHData(
            str(datadir / 'test_out.gpkg'),
            'block',
            str(datadir / 'de_pl2020_b.shp'),
            2020,
            str(datadir / 'de_cvap_2020_2020_b.csv'),
            2020
        )
        assert (datadir / 'test_out.gpkg').exists()
        with sqlite3.connect(datadir / 'test_out.gpkg') as db:
            count = db.execute('SELECT count(*) from block;').fetchone()[0]
            assert count == 20198
