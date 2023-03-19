# -*- coding: utf-8 -*-
"""
@author: claire
"""

###connect to census API

import pygris as pg
#from pygris.data import get_census
import pandas as pd
import matplotlib.pyplot as plt
#from census import Census
import requests
import geopandas as gpd
import sys

# Importing module from github
sys.path.insert(1, "C:/Users/tup48123/Documents/ApplicationDevelopment/Project")
import lobby as lb #only use base name of file


#pull table user inputted
user = pd.read_csv("data/precinct-assignments.csv")


def split_string(x):
    st = x[:2]
    return st

def cenShapes(fn):
    
    ##get state from user input
    #choose the first 2 digits
    stt = fn['GEOID20'].apply(split_string)
    global st
    st = stt[1]
            
    #from census API: shape
    #global vtd
    vtd = pg.voting_districts(state = str(stt[1]), cb = True, cache = True, year = 2020)
    
    return vtd
        

def cenDemos(fn):

    ##from census API: demographic data
    
    #####UNABLE TO GET DATA FOR BLOCKS OR CENSUS BLOCKS
    ##IT WORKS FOR TRACTS BUT NOT SMALLER GEOGRAPHIES
    
    HOST = "https://api.census.gov/data"
    
    year = "2020"
    
    dataset = "dec/pl"
    
    base_url = "/".join([HOST, year, dataset])
    
    predicates = {}

    varLst = ["NAME", "P1_001N", "P1_004N", "P1_006N", "P2_003N", "P2_005N"]
    
    predicates["get"] = ",".join(varLst)
    
    predicates["for"] = "block:*"
    
    predicates["in"] = f"state:{st}"
    
    r = requests.get(base_url, params=predicates)
    
    print(r.text)
    

    
    # x = get_census(dataset = "2020/dec/pl",
    #                         variables = "P2_001N",
    #                         params = {
    #                             "for": "block:*",
    #                             "in": f"state: {st}"
    #                         }, 
    #                         return_geoid = True, 
    #                         guess_dtypes = True)
    # return x

    # Create a Census object with your API key
    # c = Census("b42e5a4842b2207c58e2034dcfd7daaad9ca2de6")

    # # Call the get_census() function with the necessary parameters
    # data = c.sf1.get(
    #     ('NAME', "P2_001N", "P1_003N", "P1_004N", "P1_00N", "P2_003N", "P2_005N"),
    #     {'for': f'state:{st}'})
    
    # return data
   

def cenMerge(fn_shp, fn):
    
    #merge user input
    vtdMerged = fn_shp.merge(fn, on = "GEOID20")

    fig, ax = plt.subplots(1, figsize=(12, 12))
    ax.axis('off')
    vtdMerged.plot(linewidth=0.5, ax=ax, edgecolor='0.2')
    plt.show()
    
    # Group the polygons by a column with shared data
    grouped_polygons = vtdMerged.groupby('District')['geometry'].agg(lambda x: gpd.GeoSeries(x).unary_union)
    
    # Convert the grouped polygons to a GeoDataFrame
    aggregated_polygons = gpd.GeoDataFrame(geometry=grouped_polygons, crs=vtdMerged.crs)
    
    fig, ax = plt.subplots(1, figsize=(12, 12))
    ax.axis('off')
    aggregated_polygons.plot(linewidth=0.5, ax=ax, edgecolor='0.2')
    plt.show()

    
    return aggregated_polygons

    
def cenFinal(fn):
    y = cenMerge(cenShapes(fn), fn)
    
    return y

# cenFinal(user)


###FINAL OUTPUT OF SCRIPT:
    ##a geoDataFrame of the districts with aggregated demographic data 



##how to end script so the geodataframe can be sent to the next script?
# Include one controlling function named main() which is called if 
# the module is called as a script
# 
# main() should not take any parameters

# def main():
#     # Typical uses for main are to run or call a test or to run a 
#     # significant or commonly used function from the command line

# if __name__ == "__main__":
#     main()
# else:
    # optionally, module initialization code in an else-block
