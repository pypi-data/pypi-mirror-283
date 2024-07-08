# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys
import json
import numpy as np
from time import time
import pytest
from distutils import dir_util
sys.path.insert(0, os.path.realpath('../../../'))

from geostack import raster
from geostack.dataset import supported_libs
from geostack.io import geoJsonToVector, vectorToGeoJson
from geostack.gs_enums import GeometryType
from geostack.core import ProjectionParameters, REAL
from geostack.vector import Coordinate


@pytest.fixture
def datadir(tmpdir, request):
    '''
    Fixture responsible for searching a folder with the same name of test
    module and, if available, moving all contents to a temporary directory so
    tests can use them freely.

    ref: https://stackoverflow.com/questions/29627341/pytest-where-to-store-expected-data
    '''
    filename = request.module.__file__
    test_dir, _ = os.path.splitext(filename)

    if os.path.isdir(test_dir):
        dir_util.copy_tree(test_dir, str(tmpdir))

    return tmpdir


@pytest.fixture
def fileVector(datadir):
    start = time()
    file_path = datadir.join("test_data_2.geojson")
    file_vector = geoJsonToVector(file_path.strpath, dtype=REAL)
    end = time()
    print("Time taken to process file %f" % (end - start))
    return file_vector


@pytest.fixture
def proj_EPSG3111_REAL():
    proj_EPSG3111 = "(+proj=lcc +lat_1=-36 +lat_2=-38 +lat_0=-37 +lon_0=145 +x_0=2500000 +y_0=2500000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs)"
    _proj_EPSG3111_REAL = ProjectionParameters.from_proj4(proj_EPSG3111)

    return _proj_EPSG3111_REAL


@pytest.fixture
def proj_EPSG4326_REAL():
    projPROJ4_EPSG4326 = "(+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs)"
    _proj_EPSG4326_REAL = ProjectionParameters.from_proj4(projPROJ4_EPSG4326)
    return _proj_EPSG4326_REAL

def test_vec_attached(datadir, fileVector):
    testX = 144.3288723
    testY = -37.0938227

    expectedGeomIds = np.array([764, 2472, 2473, 2883, 2502, 1582])
    attachedGeomIds = fileVector.attached(Coordinate(testX, testY))

    assert np.array_equal(expectedGeomIds, attachedGeomIds)

def test_vec_nearest(datadir, fileVector):

    nearestGeoJson = """{"features": [{"geometry": {"coordinates": [144.07501, -37.28393], "type": "Point"}, "properties": {"radius": 0.05}, "type": "Feature"}], "type": "FeatureCollection"}"""
    nearestPointVector = geoJsonToVector(nearestGeoJson)
    nearestVector = fileVector.nearest(nearestPointVector.getBounds())

    with open(datadir.join("out_test_data_nearest.geojson").strpath, "w") as out:
        out.write(vectorToGeoJson(nearestVector))

    with open(datadir.join("out_test_data_nearest_point.geojson").strpath, "w") as out:
        out.write(vectorToGeoJson(nearestPointVector))

    start = time()
    fileVector.deduplicateVertices()
    end = time()
    print("Time taken to deduplicate %f" % (end - start))


def test_vec_region(datadir, fileVector):

    boundsGeoJson = """{"features": [{"geometry": {"coordinates": [[[143.73701, -37.46474], [143.73701, -37.13560], [144.41891, -37.13560], [144.41891, -37.46474], [143.73701, -37.46474]]], "type": "Polygon"}, "properties": {}, "type": "Feature"}], "type": "FeatureCollection"}"""
    boundsVector = geoJsonToVector(boundsGeoJson)

    regionVector = fileVector.region(boundsVector.getBounds())
    with open(datadir.join("out_test_data_region.geojson").strpath, "w") as out:
        out.write(vectorToGeoJson(regionVector))

    with open(datadir.join("out_test_data_bounds.geojson").strpath, "w") as out:
        out.write(vectorToGeoJson(boundsVector))


def test_vec_nearest(datadir, fileVector, proj_EPSG3111_REAL):

    fileVector = fileVector.convert(proj_EPSG3111_REAL)

    nearestGeoJson = """{"features": [{"geometry": {"coordinates": [144.07501, -37.28393], "type": "Point"}, "properties": {"radius": 0.05}, "type": "Feature"}], "type": "FeatureCollection"}"""
    nearestPointVector = geoJsonToVector(nearestGeoJson)

    nearestPointVector = nearestPointVector.convert(proj_EPSG3111_REAL)


def test_vec_mapDistance(datadir, fileVector, proj_EPSG3111_REAL):

    # test map distance when resolution and bounds are given
    testRasterise = fileVector.mapDistance(50.0, geom_type=GeometryType.LineString)
    # testRasterise.setProjectionParameters(proj_EPSG3111_REAL)

    # test map distance when a raster is given
    testRasterise2 = fileVector.mapDistance(inp_raster=testRasterise)
    assert np.allclose(testRasterise, testRasterise2)


def test_vec_mapVector(datadir, fileVector, proj_EPSG3111_REAL):

    nearestGeoJson = """{"features": [{"geometry": {"coordinates": [144.07501, -37.28393], "type": "Point"}, "properties": {"radius": 0.05}, "type": "Feature"}], "type": "FeatureCollection"}"""
    nearestPointVector = geoJsonToVector(nearestGeoJson)
    nearestPointVector = nearestPointVector.convert(proj_EPSG3111_REAL)

    # test map distance when resolution and bounds are given
    fileVector = fileVector.convert(proj_EPSG3111_REAL)
    testRasterise = fileVector.mapDistance(50.0, geom_type=GeometryType.LineString)

    testRasterise.mapVector(nearestPointVector, widthPropertyName="radius")
    testRasterise.write(datadir.join("out_test_data_distance.tif").strpath)


def test_vec_vectorise(datadir, fileVector, proj_EPSG3111_REAL, proj_EPSG4326_REAL):

    # test map distance when resolution and bounds are given
    testRasterise = fileVector.mapDistance(50.0, geom_type=GeometryType.LineString)

    contourVector = testRasterise.vectorise([10.0, 80.0])
    contourVector = contourVector.convert(proj_EPSG4326_REAL)

    with open(datadir.join("out_test_data_contour.geojson").strpath, "w") as out:
        out.write(vectorToGeoJson(contourVector))


def test_vec_sample_raster(datadir, fileVector, proj_EPSG3111_REAL):
    fileVector = fileVector.convert(proj_EPSG3111_REAL)
    testRasterise = fileVector.mapDistance(50.0, geom_type=GeometryType.LineString)

    pointVector = fileVector.convert(GeometryType.Point)
    pointVector.pointSample(testRasterise)


@pytest.mark.gdal
@pytest.mark.skipif(not supported_libs.HAS_GDAL, reason="gdal library is not installed")
def test_vec_sample_rasterfile(datadir, fileVector, proj_EPSG3111_REAL):
    fileVector = fileVector.convert(proj_EPSG3111_REAL)
    testRasterise = fileVector.mapDistance(50.0, geom_type=GeometryType.LineString)

    testRasterise.write(datadir.join("out_test_data_distance.tif").strpath)

    inpRaster = raster.RasterFile(filePath=datadir.join("out_test_data_distance.tif").strpath,
                                  name="rasterised", backend="gdal")
    inpRaster.read()

    pointVector = fileVector.convert(GeometryType.Point)
    pointVector.pointSample(inpRaster)