# -*- coding: utf-8 -*-
"""
@author: claire
"""

import os
import sys
import geopandas as gpd
import pandas as pd
import statistics as s

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

user_input = ["Polsby Popper","Schwartzberg", "Convex Hull Ratio"]

user_input = ["Polsby Popper","Schwartzberg", "Convex Hull Ratio", "Reock"]


#########OUTPUT
## minimum or average or both compactness scores
## minimum because targetting in specific districts

##make function able to accept a list of files

#ask user to specify as parameter which measure they want

#%%
def compact(measures, geo_df):
    
#user can pass multiple measures so more than 1 can be calculated
#pass in a list of measures
    d = {}
    
    if "Polsby Popper" in measures:
        pp = cm.polsby_popper(geo_df)
        d["min_pp"] = [min(pp)]
        d["mean_pp"] = [s.mean(pp)]
    
    
    if "Schwartzberg" in measures:
        schwb= cm.schwartzberg(geo_df)
        d["min_schwb"] = [min(schwb)]
        d["mean_schwb"] = [s.mean(schwb)]
        
    if "Convex Hull Ratio" in measures:
        hull= cm.c_hull_ratio(geo_df)
        d["min_hull"] = [min(hull)]
        d["mean_hull"] = [s.mean(hull)]

    if "Reock" in measures:
        reock= cm.reock(geo_df)
        d["min_reock"] = [min(reock)]
        d["mean_reock"] = [s.mean(reock)]

    # if "Polar Moment of Area" in user_input:
    #     polar_moment_of_area= cm._polar_moment_of_area(shp)
    #     d["min_polar_moment_of_area"] = [min(polar_moment_of_area)]
    #     d["mean_polar_moment_of_area"] = [s.mean(polar_moment_of_area)]
     
    # if "Mass Moment of Inertia" in user_input:
    #     mass_moment_of_inertia= cm._mass_moment_of_inertia(file)
    #     min_mass_moment_of_inertia = ["min_mass_moment_of_inertia", min(mass_moment_of_inertia)]
    #     mean_mass_moment_of_inertia = ["mean_mass_moment_of_inertia", s.mean(mass_moment_of_inertia)]
    
    # if "Moment of Inertia" in user_input:
    #     moment_of_inertia= cm.moment_of_inertia(shp)
    #     min_moment_of_inertia = ["min_moment_of_inertia", min(moment_of_inertia)]
    #     mean_moment_of_inertia = ["mean_moment_of_inertia", s.mean(moment_of_inertia)]
    
    return d

#%%
    
    
c = compact(user_input, shp)
