# -*- coding: utf-8 -*-
"""
@author: claire
"""

import os
import sys
import geopandas as gpd
import pandas as pd
import statistics as s
import tkinter as tk

#set virtual directory
os.chdir("C:/Users/tup48123/Documents/ApplicationDevelopment/Project")

# Importing module from github
sys.path.insert(1, "C:/Users/tup48123/Documents/ApplicationDevelopment/Project")
import compactness_measures as cm #only use base name of file

##

#pull user input from virtual directory
#write files to a temp folder?

#read in user inputted file
shp = gpd.read_file("data/SHP/pa_vtd_2020_bound.shp", crs="4269")

user_input = ["Polsby Popper","Schwartzberg"]


#########OUTPUT
## minimum or average or both compactness scores
## minimum because targetting in specific districts

##make function able to accept a list of files

#ask user to specify as parameter which measure they want


def user_def_measure(user_input, fn):
    
    #user can pass multiple measures so more than 1 can be calculated
    #pass in a list of measures

    if "Polsby Popper" in user_input:
        pp = cm.polsby_popper(fn)
        min_pp = ["min_pp", min(pp)]
        mean_pp = ["mean_pp", s.mean(pp)]
        
        #return pd.Series([min_pp, mean_pp])
    
    if "Schwartzberg" in user_input:
        schwb= cm.schwartzberg(fn)
        min_schwb = ["min_schwb", min(schwb)]
        mean_schwb = ["mean_schwb", s.mean(schwb)]
        
        #return pd.Series([min_schwb, mean_schwb])
    
    return pd.Series([min_pp, mean_pp]), pd.Series([min_schwb, mean_schwb])
    
    if "Convex Hull Ratio" in user_input:
        hull= cm.c_hull_ratio(fn)
        min_hull = min(hull)
        mean_hull = s.mean(hull)
        
        return min_hull, mean_hull
    


def compact(user_input, fn):
    
    y = user_def_measure(user_input, fn) #returns tuple with 2 lists
    
    for n in range(len(user_input)):
        
        if len(user_input) < 2:
            cols= {f"{y[0][0]}": y[0][1],
                  f"{y[1][0]}": y[1][1]}
            #print(cols)
            
        if len(user_input) > 1:
            cols= {f"{y[n][0][0]}": y[n][0][1],
                  f"{y[n][1][0]}": y[n][1][1]}
            #print(cols)
        
    return cols
    
    
compact(user_input, shp)
