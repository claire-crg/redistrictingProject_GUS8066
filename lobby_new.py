# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:00:38 2023

@author: tup48123
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 07:41:49 2023

@author: joshu
"""

import geopandas as gpd
import os
from get_column_info import get_gdf_geoid
from get_column_info import get_state_geoid


# def geo_check(user_gdf):
    # return 'There is no file' if len(set(geo_list)) > 1

def csv_check(plans):
    if len(plans) < 1:
        print('There are no files in this folder')
    

def shp_gdf_builder(user_gdf):
    name = os.path.splitext(os.path.basename(user_gdf))[0]
    geo_gdf = gpd.read_file(user_gdf) 
    # gpd.GeoDataFrame.to_file(shp_df, filename= "./data/" + name + "_gdf.shp")
    return geo_gdf


def check_cols_match(user_gdf, user_txt):
    txt_geoid = get_state_geoid(user_txt)[0]
    gdf_geoid = get_gdf_geoid(user_gdf, user_txt)
    if user_gdf[gdf_geoid].equals(user_txt[txt_geoid]):
        print("GEOID columns in the text and geography files match")
    else:
        print("Check if GEOID columns in the text and geography files match")


