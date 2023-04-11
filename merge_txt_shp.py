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
#import pygris as pg


#pull table user inputted
# csv = pd.read_csv("C:/Users/tup48123/Documents/ApplicationDevelopment/Project/data/precinct-assignments-cut.csv")
# shp = pg.voting_districts(state = str(state_id), cb = True, cache = True, year = 2020)

###IF user does not input shapefile or geodataframe:

def split_string(x):
    st = x[:2]
    return st

def merge_user_inputs(csv, shp):
    
    ##get state from csv user input
    #find the column with GEOID
    geoid_col = csv.applymap(lambda x: len(str(x)) > 4).all()
    district_col = csv.applymap(lambda x: len(str(x)) < 4).all()
    
    geoid_csv = geoid_col[geoid_col].index
    geoid_csv = geoid_csv[0]
    district_csv = district_col[district_col].index
    district_csv = district_csv[0]
       
    #choose the first 2 digits
    stt = csv[geoid_csv].apply(split_string)
    state_id = stt[1]
    
    ##find GEOID for shapefile user input
    geoid_col_shp = shp.applymap(lambda x: len(str(x)) > 4
                                 and str(x).startswith(str(state_id))).all()
    geoid_shp = geoid_col_shp[geoid_col_shp].index
    geoid_shp = geoid_shp[0]
    
    #merge user input
    map_merged = shp.merge(csv, left_on = geoid_shp, right_on=geoid_csv)

    # fig, ax = plt.subplots(1, figsize=(12, 12))
    # ax.axis('off')
    # vtd_merged.plot(linewidth=0.5, ax=ax, edgecolor='0.2')
    # plt.show()
    
    # Group the polygons by a column with shared data
    grouped_polygons = map_merged.dissolve(by= district_csv, as_index = False)
    
    # Convert the grouped polygons to a GeoDataFrame
    aggregated_polygons = gpd.GeoDataFrame(grouped_polygons,
                                           geometry="geometry",
                                           crs=map_merged.crs)
    
    # fig, ax = plt.subplots(1, figsize=(12, 12))
    # ax.axis('off')
    # aggregated_polygons.plot(linewidth=0.5, ax=ax, edgecolor='0.2')
    # plt.show()
    
    return aggregated_polygons


# merge_user_inputs(csv, shp)