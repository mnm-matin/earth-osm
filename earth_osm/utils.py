__author__ = "PyPSA meets Earth"
__copyright__ = "Copyright 2022, The PyPSA meets Earth Initiative"
__license__ = "MIT"

"""Utilities functions for earth_osm

This module contains utilities functions for handling OSM data.

"""


import logging
import os

import geopandas as gpd
from shapely.geometry import LineString, Point, Polygon
from earth_osm.config import primary_feature_element


logger = logging.getLogger("osm_data_extractor")
logger.setLevel(logging.INFO)


def lonlat_lookup(df_way, primary_data):
    """
    Lookup refs and convert to list of longlats
    """
    if "refs" not in df_way.columns:
        logger.warning("refs column not found")

    def look(ref):
        lonlat_row = list(map(lambda r: tuple(primary_data["Node"][str(r)]["lonlat"]), ref))
        return lonlat_row

    lonlat_list = df_way["refs"].apply(look)

    return lonlat_list

def convert_ways_points(df_way, primary_data):
    """
    Convert Ways to Point Coordinates
    """
    lonlat_list = lonlat_lookup(df_way, primary_data)
    way_polygon = list(
        map(
            lambda lonlat: Polygon(lonlat) if len(lonlat) >= 3 else Point(lonlat[0]),
            lonlat_list,
        )
    )
    area_column = list(
        map(
            int,
            round(
                gpd.GeoSeries(way_polygon)
                .set_crs("EPSG:4326")
                .to_crs("EPSG:3857")
                .area,
                -1,
            ),
        )
    )  # TODO: Rounding should be done in cleaning scripts

    def find_center_point(p):
        if p.geom_type == "Polygon":
            center_point = p.centroid
        else:
            center_point = p
        return list((center_point.x, center_point.y))

    lonlat_column = list(map(find_center_point, way_polygon))

    # df_way.drop("refs", axis=1, inplace=True, errors="ignore")
    df_way.insert(0, "Area", area_column)
    df_way.insert(0, "lonlat", lonlat_column)
