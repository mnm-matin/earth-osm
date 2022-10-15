__author__ = "PyPSA meets Earth"
__copyright__ = "Copyright 2022, The PyPSA meets Earth Initiative"
__license__ = "MIT"

"""CLI interface for earth_osm project.

This module provides a CLI interface for the earth_osm project.

"""

import argparse
import os

from earth_osm.gfk_data import get_all_valid_list, view_regions
from earth_osm.eo import get_osm_data
from earth_osm.config import primary_feature_element

def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m earth_osm` and `$ earth_osm `. 
    It parses the command line and executes the appropriate function.
    """

    parser = argparse.ArgumentParser(
        description='Earth-OSM by PyPSA-meets-Earth',
        # epilog='''Example:''',
        add_help=False) # hide default help
    subparser = parser.add_subparsers(dest='command', required=True, title='Sub Parser', description='''View Supported Regions or Extract OSM Data''')

    extract_parser = subparser.add_parser('extract', help='Extract OSM Data')

    extract_parser.add_argument('primary', choices=primary_feature_element.keys(), type=str, help='Primary Feature')

    extract_parser.add_argument('--regions',nargs="+", type=str, help='Region Identifier') # TODO: replace with region group
    extract_parser.add_argument('--features', nargs="*", type=str, help='Sub-Features')
    extract_parser.add_argument('--update', action='store_true', default=False, help='Update Data')
    extract_parser.add_argument('--mp',  action='store_true', default=True, help='Use Multiprocessing')
    extract_parser.add_argument('--data_dir', nargs="?", type=str, help='Earth Data Directory')

    
    view_parser = subparser.add_parser('view', help='View OSM Data')
    view_parser.add_argument('type', help='View Supported', choices=['regions', 'primary'])
    
    args = parser.parse_args()

    if args.command == 'view':
        print('Viewing OSM Data')
        view_regions(level=0)
    elif args.command == 'extract':
        if args.regions:
            region_list = list(args.regions)
            if not set(region_list) <= set(get_all_valid_list()):
                raise KeyError(f'Invalid Region {" ".join(set(region_list) - set(get_all_valid_list()))} , run earth_osm view regions to view valid regions')
        # elif args.coords:
        #     # TODO: change coords to shapely polygon, implement geom=True, get regions that way
        #     raise NotImplementedError('Bounding Box Region Identifier Not Implemented')

        if args.features:
            feature_list = list(args.features)
            if not set(feature_list) <= set(primary_feature_element[args.primary]):
                raise KeyError(f'Invalid Feature {" ".join(set(feature_list) - set(primary_feature_element[args.primary]))}, run earth_osm view features to view valid features')
        else:
            feature_list = primary_feature_element[args.primary]

        if args.data_dir:
            if not os.path.exists(args.data_dir):
                os.makedirs(args.data_dir, exist_ok=True)
            if os.path.isdir(args.data_dir):
                data_dir = args.data_dir
            else:
                raise NotADirectoryError(f'Invalid Data Directory {args.data_dir}')
        else:
            data_dir = os.path.join(os.getcwd(), 'earth_data')

        print('\n'.join(['',
            f'Primary Feature: {args.primary}',
            f'Sub Features: {" - ".join(feature_list)}', 
            f'Regions: {" - ".join(region_list)}',
            f'Multiprocessing = {args.mp}',
            f'Update Data = {args.update}',
            f'Data Directory = {data_dir}']))

        get_osm_data(
            region_list = region_list, 
            primary_name = args.primary,
            feature_list = feature_list,
            update = args.update,
            mp = args.mp,
            data_dir = data_dir)

    else:
        # import inquirer #https://github.com/magmax/python-inquirer
        raise NotImplementedError('Interactive Mode Not Implemented')


