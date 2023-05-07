# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 19:58:05 2023

@author: claire
"""

from merge_txt_shp import merge_user_inputs
from compactness import compact 
import pandas as pd
# import numpy as np
import geopandas as gpd
# from election_2020 import election_2020
# from historic_election_data import historic_df_builder
from fairness import fairness
import os
import glob
# import warnings
from pop_equality import pop_difference
from connect_census_api import census_gdf_data
from lobby_new import csv_check
from lobby_new import check_cols_match
# warnings.filterwarnings("ignore")


def final_dict_builder(plans_folder, shape, user_input, user_pop, user_geo, historic):
    """ Runs redistricting measures based on user inputs for each plan
        and creates a dictionary of dictionary holding the results for each plan.
    
    Parameters
    --------------------------
    
    plans_folder : List
        A list with the path (string) to the folder containing all proposed
        redistricting plans.
    shape: List
        A list with the path (string) for the geography file.
    user_input: List
        A list with the names of measures chosen by the user in the GUI interface.
    user_geo: List
        A list with the name of the geography level they are working with.
    historic: List
        A list containing the path (string) for the historic election data file.
    
    Returns
    --------------------------
    Dictionary of dictionaries
        Each sub-dictionary corresponds to a single plan from the folder of plans
        and contains the results of the user's chosen measures.
        
    Notes
    -----------------------------
    Redistricting measures:
        1. Compactness: how close to a circle is the shape of the proposed district?
        2. Fairness: does a political party have an unfair advantage in a district?
        3. Population: is the equal population requirement met?
    
    Examples
    ------------------------------
    
    >>> final_dict_builder(plans_folder, shape, user_input, user_pop, user_geo, historic)
    
    {
     plan1:{
         "eg": 0.07,
         "lmt": 0.08,
         "mean_pp": 0.2,
         "min_pp": 0.01,
         "pop_range_value" : 4048,
         "pop_mean_deviation" : 4.1,
         "pop_range_deviation" : 0.005
         },
     plan2:{
         "eg": 0.07,
         "lmt": 0.09,
         "mean_pp": 0.5,
         "min_pp": 0.2,
         "pop_range_value" : 7671,
         "pop_mean_deviation" : 4.79e-11,
         "pop_range_deviation" : 0.01
         }  
     }
    
    """
    
    compactness_tests = ['Polsby-Popper', 'Schwartzberg', 'Convex Hull Ratio', 'Reock']
    fairness_tests = ['Efficiency Gap', 'Mean-Median Difference', 'Lopsided-Margins Test']
    population_tests = ['Equal Population']
    
    #open folder with plans
    folder_string = plans_folder[0]
    plans= glob.glob(folder_string + '/*.csv')
    print(folder_string)
    
    #create empty dictionary
    dict_of_dicts = {}
    
    #check if list of plans is correct
    csv_check(plans)
    
    #open geography file as a gdf
    gdf = None
    if len(shape) > 0:
        gdf = gpd.read_file(shape[0])
        print(gdf.head(5))
    else:
        print("No geography file provided, will pull from census API")
    
    for plan in plans:
        print(plan)
        #read path and convert to dataframe
        opened_csv = pd.read_csv(plan)
        print(opened_csv.head(5))
        
        #get plan names for index
        dict_of_dicts_key= os.path.basename(plan)
        
        #merge gdf and df
        geo_df=None
        #if user inputed gdf
        if len(shape) > 0:
        ##merge csv to shapefile
            print('Already merged to user input')    
        #get path for shapefile from shape list
            # gdf = shape[0]
            #check if geoid columns match
            check_cols_match(gdf, opened_csv)
            #merge
            geo_df= merge_user_inputs(opened_csv, gdf, user_pop)
        else:
            geo_df= census_gdf_data(opened_csv, user_geo)
    
        #calculate measures
        dict_outputs= {}
        if not set(user_input).isdisjoint(set(compactness_tests)) == True:
            dict_compact= compact(user_input, geo_df) #output is a dictionary for each plan
            dict_outputs.update(dict_compact)
        # st_fips = geo_df['STATEFP20'][1]
        # print(f"st_fips = {st_fips}") 
        st_fips = 42
        if not set(user_input).isdisjoint(set(fairness_tests)) == True:
            dict_fairness= fairness(plan, historic, st_fips, user_input)
            dict_outputs.update(dict_fairness)
         #output is a dictionary for each plan
        if not set(user_input).isdisjoint(set(population_tests)) == True:
            dict_equal_pop = pop_difference(geo_df, user_pop)
            dict_outputs.update(dict_equal_pop)
        
        #create inner dictionary to join to dict of dicts
        inner_dict = {}
        
        values_test = list(dict_outputs.values())
        keys_test = list(dict_outputs.keys())
        
        
        for plan_index in range(len(values_test)):
    
            inner_dict[keys_test[plan_index]] = values_test[plan_index]
            
            dict_of_dicts[f'{dict_of_dicts_key}'] = inner_dict
            
    return dict_of_dicts

