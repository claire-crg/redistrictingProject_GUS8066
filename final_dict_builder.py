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
# from fairness import fairness
import os
import glob
# import warnings
from pop_equality import pop_difference
from connect_census_api import census_gdf_data
import connect_census_api

# warnings.filterwarnings("ignore")

wd = os.getcwd()

path = wd
# plans = glob.glob(os.path.join(path + "/data/plans/*.csv"))
plans = ["C:/Users/tup48123/Documents/ApplicationDevelopment/redistrictingProject_GUS8066-main/data/new_plan.csv",
"C:/Users/tup48123/Documents/ApplicationDevelopment/redistrictingProject_GUS8066-main/data/pa_no_splits.csv",
"C:/Users/tup48123/Documents/ApplicationDevelopment/redistrictingProject_GUS8066-main/data/precinct-assignments.csv",
"C:/Users/tup48123/Documents/ApplicationDevelopment/redistrictingProject_GUS8066-main/data/under_max_competitive.csv"]

gdf = gpd.read_file('C:/Users/tup48123/Documents/ApplicationDevelopment/Project/data/SHP/pa_vtd_2020_bound.shp')

user_input = ["Polsby Popper","Schwartzberg", "Convex Hull Ratio", "Reock"]


# plan = pd.read_csv("./data/pa_no_splits.csv")

user_input=[]
plan=[]
shape=[]
historic =[]
geo_list =['County', 'County Subdivision', 'Place', 'Tract', 'Voting District']
user_geo = ['Voting District']
user_pop = ['tot_pop']
pop_column_options = []

test = final_dict_builder(plans, shape)

def final_dict_builder(plans_folder, *args):
    ######main function calling all functions
    dict_of_dicts = {}
    
    for plan in plans:
        #read path and convert to dataframe
        opened_csv = pd.read_csv(plan)
        #get plan names for index
        dict_of_dicts_key= os.path.basename(plan)
        
        #if user inputed gdf
        geo_df=None
        if len(shape) > 0:
        # ##merge csv to shapefile
            geo_df= merge_user_inputs(opened_csv, test, user_pop)
        else:
            geo_df= census_gdf_data(opened_csv, user_geo)
    
        #calculate measures
        # dict_outputs= {}
        dict_compact= compact(user_input, test) #output is a dictionary for each plan
        #dict_fairness= fairness(plan) #output is a dictionary for each plan
        dict_equal_pop = pop_difference(test, pop_column)
        
        dict_compact.update(dict_fairness) 
        
        #create inner dictionary to join to dict of dicts
        inner_dict = {}
        
        values_test = list(dict_compact.values())
        keys_test = list(dict_compact.keys())
        
        
        for plan_index in range(len(values_test)):
    
            inner_dict[keys_test[plan_index]] = values_test[plan_index]
            
            dict_of_dicts[f'{dict_of_dicts_key}']= inner_dict
            
    return dict_of_dicts

test = final_dict_builder(plans, shp, user_input, pop_column="tot_pop")

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