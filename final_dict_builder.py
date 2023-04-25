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


def final_dict_builder(plans_folder, *args):
    wd = os.getcwd()
    path = os.path.join(wd_path + "/data/*.csv")
    plans = glob.glob(path)

    ######main function calling all functions
    dict_of_dicts = {}
    
    #check if list of plans is correct
    csv_check(plans)
    
    #open geography file as a gdf
    gdf = None
    if len(shape) > 0:
        gdf = gpd.read_file(shape[0])
    else:
        print("No geography file provided, will pull from census API")
    
    for plan in plans:
        #read path and convert to dataframe
        opened_csv = pd.read_csv(plan)
        #get plan names for index
        dict_of_dicts_key= os.path.basename(plan)
        
        #merge gdf and df
        geo_df=None
        #if user inputed gdf
        if len(shape) > 0:
        ##merge csv to shapefile
            #get path for shapefile from shape list
            gdf = shape[0]
            #check if geoid columns match
            check_cols_match(gdf, opened_csv)
            #merge
            geo_df= merge_user_inputs(opened_csv, gdf, user_pop)
        else:
            geo_df= census_gdf_data(opened_csv, user_geo)
    
        #calculate measures
        # dict_outputs= {}
        dict_compact= compact(user_input, geo_df) #output is a dictionary for each plan
        dict_fairness= fairness(plan) #output is a dictionary for each plan
        dict_equal_pop = pop_difference(geo_df, user_pop)
        
        
        dict_compact.update(dict_fairness)
        dict_compact.update(dict_equal_pop)
        
        #create inner dictionary to join to dict of dicts
        inner_dict = {}
        
        values_test = list(dict_compact.values())
        keys_test = list(dict_compact.keys())
        
        
        for plan_index in range(len(values_test)):
    
            inner_dict[keys_test[plan_index]] = values_test[plan_index]
            
            dict_of_dicts[f'{dict_of_dicts_key}'] = inner_dict
            
    return dict_of_dicts

