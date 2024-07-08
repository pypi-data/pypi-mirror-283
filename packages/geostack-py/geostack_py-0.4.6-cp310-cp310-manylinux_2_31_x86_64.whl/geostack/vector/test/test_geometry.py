# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys
sys.path.insert(0, os.path.realpath('../../../'))

from geostack.vector import Coordinate, BoundingBox

def test_create_coordinate():
    c0 = Coordinate(0.0, 0.0)
    assert (c0.p == 0.0) & (c0.q == 0.0)

def test_edit_coordinate():
    c0 = Coordinate(0.0, 0.0)
    c0.p = 1.0
    assert (c0.p == 1.0) & (c0.q == 0.0)

def test_coord_equality():
    c0 = Coordinate(0.0, 0.0)
    c1 = Coordinate(1.0, 1.0)
    assert not(c0 == c1)

def test_coord_inequality():
    c0 = Coordinate(0.0, 0.0)
    c1 = Coordinate(1.0, 1.0)
    assert c0 != c1

def test_bbox_from_coords():
    c0 = Coordinate(0.0, 0.0)
    c1 = Coordinate(1.0, 1.0)
    b1 = BoundingBox(min_coordinate=c0, max_coordinate=c1)
    assert (b1.min == c0) & (b1.max == c1)

def test_bbox_from_bbox():
    c0 = Coordinate(0.0, 0.0)
    c1 = Coordinate(1.0, 1.0)
    b1 = BoundingBox(min_coordinate=c0, max_coordinate=c1)
    b2 = BoundingBox(input_bbox=b1)
    assert (b2.min == c0) & (b2.max == c1)

def test_bbox_equality():
    c0 = Coordinate(0.0, 0.0)
    c1 = Coordinate(1.0, 1.0)
    b1 = BoundingBox(min_coordinate=c0, max_coordinate=c1)
    b2 = BoundingBox(input_bbox=b1)
    assert b1 == b2

def test_bbox_inequality():
    c0 = Coordinate(0.0, 0.0)
    c1 = Coordinate(1.0, 1.0)
    b1 = BoundingBox(min_coordinate=c0, max_coordinate=c1)
    b2 = BoundingBox(input_bbox=b1)
    assert not(b1 != b2)

def test_change_max_coord_bbox():
    c0 = Coordinate(0.0, 0.0)
    c1 = Coordinate(1.0, 1.0)
    c2 = Coordinate(2.0, 2.0)
    b1 = BoundingBox(min_coordinate=c0, max_coordinate=c1)
    b2 = BoundingBox(input_bbox=b1)
    b2.max = c2
    assert (b2.min == c0) & (b2.max == c2)
