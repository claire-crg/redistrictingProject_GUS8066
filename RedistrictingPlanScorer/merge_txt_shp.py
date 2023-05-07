# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 16:24:39 2023

@author: claire
"""

## function to merge district assignments to shapefile

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
from pop_equality import get_pop_col
from get_column_info import chng_dist_col, get_state_geoid, get_gdf_geoid
#import pygris as pg


###IF user provides a shapefile, use the merge_user_inputs function


def merge_user_inputs(user_txt, geo_gdf, user_input_demographics):
    """ Merges district assignment and geography files provided by user,
        and aggregates polygons by district assignment.
    
    Parameters
    --------------------------
    
    user_txt : DataFrame
        District Assignment file provided by user.
        Contains two columns: geography level, district assignment.
        Geography level in user_txt must match user_geo_type.    
    geo_gdf : GeoDataFrame
        Geography file provided by user, opened outside this function as GDF.
    user_input_demographics: list
        Column names of demographic columns in user inputted GeoDataFrame.
        Names provided by user in GUI interface.

    
    Returns
    --------------------------
    GeoDataFrame
        GeoDataFrame with aggregated polygons and demographic data
        by district assignment. Represents proposed redistricting plan.
        
    
    Examples
    ------------------------------
      
    >>> merge_user_inputs(plan2, PA_places, ["tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop"]).columns
    
    "GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district", "geometry"
    
    """
    
    #user inputted text geoid and state id
    geo_state = get_state_geoid(user_txt)
    
    #geoid csv
    geoid_csv = geo_state[0]
    
    #state id
    state_id = geo_state[1]
    
    #csv district column
    user_txt = chng_dist_col(user_txt)
    district_csv = 'district_csv'
    
    ##find GEOID for shapefile user input
    # geoid_col_shp = geo_gdf.applymap(lambda x: len(str(x)) > 4 and str(x).startswith(str(state_id))).all()
    # geoid_shp = geoid_col_shp[geoid_col_shp].index[0]
    geoid_shp = get_gdf_geoid(geo_gdf, user_txt)
        
    #merge user input
    map_merged = geo_gdf.merge(user_txt, left_on = geoid_shp, right_on=geoid_csv)

    ##aggregate
   
    #group data by district
    #make sure data columns are integers
    for i in map_merged.columns:
        if i in user_input_demographics:
            map_merged[i] = map_merged[i].apply(lambda x: int(x))
    #now group
    # print(map_merged.columns)    
    grouped_data = map_merged.groupby(district_csv)[user_input_demographics].sum()

    
    # Group the polygons by a column with shared data
    #first remove the demographic data so it will not be duplicated after we add the aggregated data
    cols_to_select = ~map_merged.columns.isin(user_input_demographics)
    map_merged = map_merged.loc[:, cols_to_select]
    
    #group
    grouped_polygons = map_merged.dissolve(by= district_csv, as_index = False)
    #grouped_polygons = map_merged.groupby(district_csv)['geometry'].agg(lambda x: gpd.GeoSeries(x).unary_union)

    #merge grouped data to grouped polygons
    grouped_polygons = pd.merge(grouped_polygons, grouped_data, how='inner', on=district_csv).reset_index()

    # Convert the grouped polygons to a GeoDataFrame
    aggregated_polygons = gpd.GeoDataFrame(grouped_polygons,
                                           geometry="geometry",
                                           crs=map_merged.crs)
    return aggregated_polygons


