# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:29:19 2023

@author: tup48123
"""

import pygris as pg
#from pygris.data import get_census
import pandas as pd
import matplotlib.pyplot as plt
#from census import Census
import requests
import geopandas as gpd
import numpy as np
from get_column_info import get_dist_col
from get_column_info import get_state_geoid
from get_column_info import get_dist_col

#load files to test functions
# user_txt = pd.read_csv("C:/Users/tup48123/Documents/ApplicationDevelopment/Project/data/precinct-assignments-cut.csv")
#user_geo_type is the list generated from the user input in the GUI
# user_geo_type = ['Voting District']   


#get geography type for building blocks to create voting districts
def get_geo(user_geo_type, user_txt):
    """ Gets GeoDataFrame from Census API based on user's choice of geography level.
    Uses pygris module.
    
    Parameters
    --------------------------
    
    user_geo_type : list
        Geography level used as building blocks to create voting districts,
        chosen by user in GUI interface- passed as a list.
    user_txt : DataFrame
        District Assignment file provided by user.
        Contains two columns: geography level, district assignment.
        Geography level in user_txt must match user_geo_type.
    
    Returns
    --------------------------
    list
        The list contains 4 elements:
            a. GeoDataFrame of geography level from Census API,
            b. user_geo_type,
            c. GEOID column name in user_txt,
            d. GEOID column name in GeoDataFrame from the Census API.
    
    Notes
    -----------------------------
    Steps:
        1. Gets the state code based on the first 2 digits of value in user_txt GEOID.
        2. Pulls GeoDataFrame from Census API using geography type from user_geo_type
            and state code.
        3. Gets GEOID column name in the GeoDataFrame.
    
    Examples
    ------------------------------
      
    >>> get_geo('Voting District', plan1)
    
    [{GeoDataFrame},
     'Voting District',
     'id',
     'GEOID20']

    """
    
    #get geoid from user file
    user_geoid= get_state_geoid(user_txt)
    #geoid from user inputted txt file
    geoid_user = user_geoid[0]
    #state id from geoid
    state_id = user_geoid[1]
            
    #from census API: shape    
    geo_types = ['County', 'County Subdivision', 'Place', 'Tract', 'Voting District']
    
    #user_geo_type is the list generated from the user input in the GUI
    geo = None
    if user_geo_type[0] in geo_types:
        if user_geo_type[0] == geo_types[0]:
            geo = pg.counties(state = str(state_id), cb = True, cache = True, year = 2020)
        elif user_geo_type[0] == geo_types[1]:
            geo = pg.county_subdivisions(state = str(state_id), cb = True, cache = True, year = 2020)
        elif user_geo_type[0] == geo_types[2]:
            geo = pg.places(state = str(state_id), cb = True, cache = True, year = 2020)
        elif user_geo_type[0] == geo_types[3]:
            geo = pg.tracts(state = str(state_id), cb = True, cache = True, year = 2020)
        elif user_geo_type[0] == geo_types[4]:
            geo = pg.voting_districts(state = str(state_id), cb = True, cache = True, year = 2020)
    else:
        print("Geography not given")
    
    #get geoid from census geography
    x = [col for col in geo.columns if "GEOID" in col]
    for col in x:
        geoid_cen = [col for row in geo[col] if row.startswith(str(state_id))]
    
    return geo, user_geo_type, geoid_user, geoid_cen[0]
    



#get population and demographic data from census    
def get_data(user_geo_type, user_txt):
    """ Gets demographic data from Census API based on user's choice of geography level.
    
    Parameters
    --------------------------
    
    user_geo_type : list
        Geography level used as building blocks to create voting districts,
        chosen by user in GUI interface- passed as a list.
    user_txt : DataFrame
        District Assignment file provided by user.
        Contains two columns: geography level, district assignment.
        Geography level in user_txt must match user_geo_type.
    
    Returns
    --------------------------
    DataFrame
        Total population and racial data by user's chosen geography level
        from the Decennial Census.
    
    Notes
    -----------------------------
    Steps:
        1. Gets GEOID column name in the GeoDataFrame.
        2. Gets the state code based on the first 2 digits of value in user_txt GEOID.
        2. Pulls data from Census API using geography type from user_geo_type
            and state code.
        
    
    Examples
    ------------------------------
      
    >>> get_data('County Subdivision', plan1).columns
    
    "GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop"

    """
    
    # #get gdf from census, geo level
    # geo_data = get_geo(user_geo_type, user_txt)
    
    #get geoid from user input and state code
    user_geoid= get_state_geoid(user_txt)
    
    #define state id
    state_id = user_geoid[1]
    
    #define user geography input ex: 'Voting District'
    user_geo = user_geo_type[0].lower()
    # user_geo = geo_data[1][0].lower()
    
    #get data from census
    HOST = "https://api.census.gov/data"
    
    base_url = "/".join([HOST, "2020", "dec/pl"])
    
    predicates = {}
    
    varLst = ["NAME", "P1_001N", "P2_002N", "P2_005N", "P2_006N", "P2_008N"]
    
    predicates["get"] = ",".join(varLst)
    
    predicates["for"] = f"{user_geo}:*"
    
    predicates["in"] = f"state: {state_id}"
    
    #save data
    cen_data = requests.get(base_url, params=predicates)
    
    #convert to json
    data_json = cen_data.json()
    
    #convert to dataframe
    data_df = pd.DataFrame(data_json[1:], columns=data_json[0])
    
    #change column names
    col_names = ["tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop"]
    
    for i in range(len(col_names)):
        data_df= data_df.rename(columns={data_df.columns[i+1]: col_names[i]})
    
    return data_df
    

#merge census data to district assignment file
def join_cen_assgn(user_txt, geo_data, user_geo_type):
    """ Join demographic data from Census API and district assignment file.
    
    Parameters
    --------------------------
    
    user_txt : DataFrame
        District Assignment file provided by user.
        Contains two columns: geography level, district assignment.
        Geography level in user_txt must match user_geo_type.
    geo_data : list
        Output from get_geo():
            [GeoDataFrame, user_geo_type,
             GEOID column name in user_txt, GEOID column name in GeoDataFrame]
    user_geo_type : list
        Geography level used as building blocks to create voting districts,
        chosen by user in GUI interface- passed as a list.
    
    Returns
    --------------------------
    DataFrame
        DataFrame with district assignment column added to demographic data
        by geography level.
    
    Notes
    -----------------------------
    Steps:
        1. Gets demographic data from Census API using get_data() 
        2. Gets GEOID column name in the user_txt and geography level from user input.
        3. Builds GEOID in Census DataFrame using state code, county code, and
            chosen geography code.
        4. Merges Census data and district assignment file.
        
    
    Examples
    ------------------------------
      
    >>> join_cen_assgn(plan1, geo_data, 'County Subdivision').columns
    
    "GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district"

    """
    
    #get census demographic data
    cen_data = get_data(user_geo_type, user_txt)
    
    #get geoid from user input geo
    geoid_user_txt = geo_data[2]
    
    ##get geoid from census data
    #geoid_cen = geo_data[3]
    
    #get level name
    geo_level = geo_data[1][0].lower()
    
    ##build geoid from census data to match user input
    cen_data['GEOID'] = cen_data[['state', 'county', geo_level]].apply(lambda x: ''.join(x.astype(str)).replace(' ', ''), axis=1)
    
    #check if geoid columns match
    #if cen_data['GEOID'].equals(user_txt[geo_user_txt]):
    data_merged = user_txt.merge(cen_data, left_on = geoid_user_txt, right_on = "GEOID")
    
    return data_merged
    

#merge census data to geography
def merge_cendata_geo(data_merged, geo_data):
    """ Join merged demographic and district assignment data to GeoDataFrame.
    
    Parameters
    --------------------------
    
    data_merged : DataFrame
        Output from join_cen_assgn():
            District Assignment file merged with demographic Census data.
    geo_data : list
        Output from get_geo():
            [GeoDataFrame, user_geo_type,
             GEOID column name in user_txt, GEOID column name in GeoDataFrame]
    
    Returns
    --------------------------
    GeoDataFrame
        GeoDataFrame with district assignment column and demographic data
        by geography level.
    
    Notes
    -----------------------------
    Steps:
        1. Gets GeoDataFrame from geo_data[0], GEOID column name from district
            assignment file, and GEOID column name from Census GeoDataFrame.
        2. Merges Census data and GeoDataFrame.
        
    
    Examples
    ------------------------------
      
    >>> merge_cendata_geo(data_merged, geo_data).columns
    
    "GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district", "geometry"

    """
    
    #get shapes from census
    geo = gpd.GeoDataFrame(geo_data[0], geometry='geometry', crs='EPSG:4269')

    #geoid from user text
    geoid_user_txt = geo_data[2]
    # print(geoid_user_txt)
    #geoid from cen geo
    geoid_cen = geo_data[3]
    # print(geoid_cen)
    ##merge user input
    
    #check for leading 0s
    #geoid from census shapefile should match 
    max_len_user = max(data_merged['GEOID'].apply(len))
    max_len_cen = max(geo[geoid_cen].apply(len))
    
    # #add leading zeros if necessary
    if max_len_user == max_len_cen:
        data_merged[geoid_user_txt] = data_merged['GEOID'].apply(lambda x: str(x).zfill(max_len_user))
        geo[geoid_cen] = geo[geoid_cen].apply(lambda x: str(x).zfill(max_len_cen))


    #merge user text input to gdf from census
    geo_merged = geo.merge(data_merged, left_on = geoid_cen, right_on = geoid_user_txt)
    # geo_merged = geo.merge(data_merged, on = str(geoid_user_txt))
   
    return geo_merged
    

def agg_geo(data_merged, geo_data, user_txt):
    """ Aggregates polygons in GeoDataFrame by district assignment.
    
    Parameters
    --------------------------
    
    data_merged : DataFrame
        Output from join_cen_assgn():
            District Assignment file merged with demographic Census data.
    geo_data : list
        Output from get_geo():
            [GeoDataFrame, user_geo_type,
             GEOID column name in user_txt, GEOID column name in GeoDataFrame]
    user_txt: DataFrame
        District Assignment file provided by user.
        Contains two columns: geography level, district assignment.
        Geography level in user_txt must match user_geo_type.
    
    Returns
    --------------------------
    GeoDataFrame
        GeoDataFrame with aggregated polygons by district assignment. Represents
        proposed redistricting plan.
    
    Notes
    -----------------------------
    Steps:
        1. Merges Census data and GeoDataFrame.
        2. Aggregates polygons by district assignment.
        3. Aggregates demographic data by district assignment.
        4. Merges aggregated data to aggregated polygons
        
    
    Examples
    ------------------------------
      
    >>> agg_geo(data_merged, geo_data, user_txt).columns
    
    "GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district", "geometry"

    """
    
    #merge census data to geography
    geo = merge_cendata_geo(data_merged, geo_data)

    #keep same CRS as when downloaded from census
    geo.to_crs('EPSG:4269')
    
    #get the assignments column from the user txt file
    districts = get_dist_col(user_txt)
    
    ## Group the polygons by a column with shared data
    grouped_polygons = geo.dissolve(by=districts, as_index=False)
    grouped_polygons = grouped_polygons[[districts, 'geometry']]
    
    # grouped_polygons = geo.groupby(districts)['geometry'].agg(lambda x: gpd.GeoSeries(x).unary_union)

    #Group census data by district
    #convert columns to integers
    col_names = ["tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop"]
    for i in geo.columns:
        if i in col_names:
            geo[i] = geo[i].apply(lambda x: int(x))
        
    grouped_data = geo.groupby(districts)[col_names].sum()
    
    ##merge aggregated data to grouped polygons
    # grouped_polygons = gpd.GeoDataFrame(grouped_polygons, geometry='geometry')
    grouped_polygons = grouped_polygons.merge(grouped_data, on=districts)
    # grouped_polygons = pd.merge(grouped_polygons[[districts, 'geometry']], grouped_data, how='inner', on=districts).reset_index()
    
    # Convert the grouped polygons to a GeoDataFrame
    aggregated_polygons = gpd.GeoDataFrame(grouped_polygons, crs='EPSG:4269')
    
    return aggregated_polygons 


####FUNCTIONS TO CALL TO GET AGGREGATED POLYGONS

def census_gdf_data(user_txt, user_geo_type):
    """ Produces GeoDataFrame with aggregated polygons by district assignment.
        Calls functions in this module based on workflow order.
    
    Parameters
    --------------------------
    
    user_txt : DataFrame
        District Assignment file provided by user.
        Contains two columns: geography level, district assignment.
        Geography level in user_txt must match user_geo_type.    
    user_geo_type : list
        Geography level used as building blocks to create voting districts,
        chosen by user in GUI interface- passed as a list.

    
    Returns
    --------------------------
    GeoDataFrame
        GeoDataFrame with aggregated polygons and demographic data
        by district assignment. Represents proposed redistricting plan.
        
    
    Examples
    ------------------------------
      
    >>> census_gdf_data(plan2, 'Places').columns
    
    "GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district", "geometry"
    
    """

    #do this outside function so we don't pull from api too many times and slow down process
    geo_data_list = get_geo(user_geo_type, user_txt)
    #do this outside function so we don't pull from api too many times and slow down process
    data_merged = join_cen_assgn(user_txt, geo_data_list, user_geo_type)
    #aggregated polygons with census data
    agg_poly = agg_geo(data_merged, geo_data_list, user_txt)

    return agg_poly

