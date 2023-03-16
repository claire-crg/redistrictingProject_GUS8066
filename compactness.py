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
import connect_census as cen

##

##first on the to do list: where are we storing the outputs of each script and how are we pulling them into the next script?
#pull user input from virtual directory
#write files to a temp folder?

#read in user inputted file
shp = gpd.read_file("data/SHP/pa_vtd_2020_bound.shp", crs="4269")


#second on the to do list:
##ask user to specify as parameter which measure they want
##make function able to accept a list of files


#########OUTPUT
## minimum or average or both compactness scores
## minimum because targetting in specific districts


def userDefMeasure(user_input, fn):
    
    ##since this script is coming in after the census pull, we don't need to
    ##differentiate whether the input is text or shapefile

    if user_input == "Polsby Popper":
        pp = cm.polsby_popper(fn)
        min_pp = ["min_pp", min(pp)]
        mean_pp = ["mean_pp", s.mean(pp)]
        
        return min_pp, mean_pp
    
    elif user_input == "Schwartzberg":
        schwb= cm.schwartzberg(fn)
        min_schwb = min(schwb)
        mean_schwb = s.mean(schwb)
        
        return min_schwb, mean_schwb
    
    elif user_input == "Convex Hull Ratio":
        hull= cm.c_hull_ratio(fn)
        min_hull = min(hull)
        mean_hull = s.mean(hull)
        
        return min_hull, mean_hull
    


def compact(user_input, fn):
    
    y = userDefMeasure(user_input, fn) #returns tuple with 2 lists
    
    data = {"planID": [1], #when more plans are added, column will have to populate ints for # of plans
            f"{y[0][0]}": [y[0][1]],
            f"{y[1][0]}": [y[1][1]]
            }
    
    df = pd.DataFrame(data)
    
    return df



#pass user file through compact()
compact("Polsby Popper", shp)

        
