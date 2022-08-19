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
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

__author__ = "Stuart C. Naifeh"
__contact__ = "stuart@cryptodira.org"
__copyright__ = "Copyright (c) 2022, Stuart C. Naifeh"
__license__ = "GPLv3"
__version__ = "0.0.1"

# noinspection PyPep8Naming


def classFactory(iface):  # pylint: disable=invalid-name
    """Create an instance of the RDHImport plugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .rdh_import import RDHImport  # pylint: disable=import-outside-toplevel
    return RDHImport(iface)
