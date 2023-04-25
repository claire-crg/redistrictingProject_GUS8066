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
from get_column_info import get_dist_col, get_state_geoid, get_dist_col
#import pygris as pg


#pull table user inputted
csv = pd.read_csv("C:/Users/tup48123/Documents/ApplicationDevelopment/Project/data/precinct-assignments-cut.csv")
#shp = pg.voting_districts(state = str(state_id), cb = True, cache = True, year = 2020)
geo_gdf = gpd.read_file("C:/Users/tup48123/Documents/ApplicationDevelopment/Project/data/SHP/pa_vtd_2020_bound.shp")

###IF user provides a shapefile, use the merge_user_inputs function


def merge_user_inputs(user_txt, geo_gdf, user_input_pop_col):
    
    #user inputted text geoid and state id
    geo_state = get_state_geoid(user_txt)
    
    #geoid csv
    geoid_csv = geo_state[0]
    
    #state id
    state_id = geo_state[1]
    
    #csv district column
    district_csv = get_dist_col(user_txt)
    
    ##find GEOID for shapefile user input
    geoid_col_shp = geo_gdf.applymap(lambda x: len(str(x)) > 4 and str(x).startswith(str(state_id))).all()
    geoid_shp = geoid_col_shp[geoid_col_shp].index[0]
    
    #merge user input
    map_merged = geo_gdf.merge(user_txt, on = geoid_shp)
    

    # fig, ax = plt.subplots(1, figsize=(12, 12))
    # ax.axis('off')
    # vtd_merged.plot(linewidth=0.5, ax=ax, edgecolor='0.2')
    # plt.show()

    ##aggregate
    #get pop column
    pop_col = get_pop_col(user_input_pop_col[0], geo_gdf)
    #group data by district
    grouped_data = geo_gdf.groupby(district_csv)[pop_col].sum()
    
    # Group the polygons by a column with shared data
    grouped_polygons = map_merged.dissolve(by= district_csv, as_index = False)
    # grouped_polygons = map_merged.groupby(district_csv)['geometry'].agg(lambda x: gpd.GeoSeries(x).unary_union)
     
    #merge grouped data to grouped polygons
    grouped_polygons = pd.merge(grouped_polygons, grouped_data, how='inner', on=district_csv).reset_index()

    # Convert the grouped polygons to a GeoDataFrame
    aggregated_polygons = gpd.GeoDataFrame(grouped_polygons,
                                           geometry="geometry",
                                           crs=map_merged.crs)
    
    # fig, ax = plt.subplots(1, figsize=(12, 12))
    # ax.axis('off')
    # aggregated_polygons.plot(linewidth=0.5, ax=ax, edgecolor='0.2')
    # plt.show()
    
    return aggregated_polygons


test1 = merge_user_inputs(opened_csv, test, user_pop)

