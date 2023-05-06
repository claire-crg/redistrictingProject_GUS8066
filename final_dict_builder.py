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


# # gdf = 'C:/Users/tup48123/Documents/ApplicationDevelopment/Project/data/vtd_gdf.gpkg'
# user_input = ["Polsby Popper","Schwartzberg", "Convex Hull Ratio", "Reock"]
# # plan=[]
# shape=[]
# # historic =[]
# # geo_list =['County', 'County Subdivision', 'Place', 'Tract', 'Voting District']
# user_geo = ['Voting District']
# user_pop = ['tot_pop']
# # pop_column_options = []

# wd = os.getcwd()
# wd_path = r'C:/Users/tup48123/Documents/ApplicationDevelopment/redistrictingProject_GUS8066-main'
# path = os.path.join(wd_path + "/data/*.csv")
# plans = glob.glob(path)


def final_dict_builder(plans_folder, shape, user_input, user_pop, user_geo, historic):
    
    folder_string = plans_folder[0]
    plans= glob.glob(folder_string + '/*.csv')
    print(folder_string)
    ######main function calling all functions
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
        # dict_outputs= {}
 
        dict_compact= compact(user_input, geo_df) #output is a dictionary for each plan
        st_fips = geo_df['STATEFP20'][1]
        print(f"st_fips = {st_fips}")       
        dict_fairness= fairness(plan, historic, st_fips) #output is a dictionary for each plan
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



# test = final_dict_builder(plans, shape, user_input, user_pop, user_geo)

 ####main function for 1 measure to create a dict of dicts
#this one works       
# for plan in plans:  

#     key= os.path.basename(plan)
     
#     inner_dict = {}
    
#     test=fairness(plan)
        
#     values_test = list(test.values())
#     keys_test = list(test.keys())
    
#     for plan_index in range(len(values_test)):

#         inner_dict[keys_test[plan_index]] = values_test[plan_index]
        
#         dict_of_dicts[f'{key}']= inner_dict