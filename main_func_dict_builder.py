
from merge_txt_shp import merge_user_inputs
from compactness import compact 
import pandas as pd
import numpy as np
import geopandas as gpd
from election_2020 import election_2020
from historic_election_data import historic_df_builder
from fairness import fairness
import os
import glob
import warnings

# warnings.filterwarnings("ignore")

wd = os.getcwd()

path = wd
plans = glob.glob(os.path.join(path + "/data/plans/*.csv"))

shp = gpd.read_file('./data/tl_2020_42_vtd20_gdf.shp')

user_input = ["Polsby Popper","Schwartzberg", "Convex Hull Ratio", "Reock"]


# plan = pd.read_csv("./data/pa_no_splits.csv")


######main function calling all functions
dict_of_dicts = {}

for plan in plans:
    #read path and convert to dataframe
    opened_csv = pd.read_csv(plan)
    #get plan names for index
    dict_of_dicts_key= os.path.basename(plan)
    #merge csv to shapefile
    geo_df= merge_user_inputs(opened_csv, shp)

    #put each function outputs in a list
    #measure_functions = list(compact(plan), fairness(plan))
    dict_outputs= {}
    dict_compact= compact(user_input, geo_df) #output is a dictionary for each plan
    dict_fairness= fairness(plan) #output is a dictionary for each plan
    
    dict_compact.update(dict_fairness) 
    
    #create inner dictionary to join to dict of dicts
    inner_dict = {}
    
    values_test = list(dict_compact.values())
    keys_test = list(dict_compact.keys())
    
    
    for plan_index in range(len(values_test)):

        inner_dict[keys_test[plan_index]] = values_test[plan_index]
        
        dict_of_dicts[f'{dict_of_dicts_key}']= inner_dict
        
 

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
