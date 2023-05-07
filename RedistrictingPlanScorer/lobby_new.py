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
    """ Check that district assignment files were provided.
    
    Parameters
    --------------------------
    plans: List
        List with the path strings for the plans.
    
    Returns
    --------------------------
    String
        Error message
    
    """
    
    if len(plans) < 1:
        print('There are no files in this folder')
    

def check_cols_match(user_gdf, user_txt):
    """ Check if GEOID columns match.
    
    Parameters
    --------------------------
    user_gdf: GeoDataFrame
        Geography file provided by user, opened outside this function as GDF.
    user_txt: DataFrame
        User inputted district assignment file.
        Contains two columns: geography level, district assignment.
        Geography level in user_txt must match user_geo_type.  
    
    Returns
    --------------------------
    String
        Either update or error message.
    
    """
    txt_geoid = get_state_geoid(user_txt)[0]
    gdf_geoid = get_gdf_geoid(user_gdf, user_txt)
    if user_gdf[gdf_geoid].equals(user_txt[txt_geoid]):
        print("GEOID columns in the text and geography files match")
    else:
        print("Check if GEOID columns in the text and geography files match")


