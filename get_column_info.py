# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 17:24:09 2023

@author: tup48123
"""


#get state code
def split_string(x):
    st = x[:2]
    return st


def get_state_geoid(user_txt):
    ##get state from user input
    #find the column with GEOID
    geoid_col = user_txt.applymap(lambda x: len(str(x)) > 4).all()
    
    #get the name of the GEOID column
    geoid = geoid_col[geoid_col].index[0]

    #choose the first 2 digits
    stt = user_txt[geoid].apply(split_string)
    state_id = stt[1]
    
    return geoid, state_id



def get_dist_col(user_txt):
    #find the column with GEOID
    district_col = user_txt.applymap(lambda x: len(str(x)) < 4).all()
    district_csv = district_col[district_col].index[0]
    
    return district_csv