# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 15:15:28 2023

@author: claire
"""

import geopandas as gpd

# when function is called in the main function,
# identify which column is the population column
# ask user to specify which column it is?

#read in user inputted file
shp = gpd.read_file("C:/Users/tup48123/Documents/ApplicationDevelopment/Project/data/SHP/pa_vtd_2020_bound.shp", crs="4269")


# see if population is equal in each polygon

def equal_population(gdf, pop_column):

    # empty dictionary to save results
    d = {}
    
    #make sure it is passed as a string
    pop_column = str(pop_column)

    # initialize a variable to keep track of the previous value
    prev_value = None

    # iterate through the rows of the GeoDataFrame
    for index, row in gdf.iterrows():

        # check if the value in the current row is the same as the previous value
        if row[pop_column] == prev_value:
            # equality = True
            d["equal_pop"] = 'Yes'

        elif row[pop_column] != prev_value:
            # equality = False
            d["equal_pop"] = 'No'

    return d


# if congressional maps,
# population must be exactly equal, allowance to be off by 1 or 2 people

def pop_difference(gdf, pop_column):
    
    #make sure it is passed as a string
    pop_column = str(pop_column)

    equality = equal_population(gdf, pop_column)
    
    d={}

    if equality['equal_pop'] == 'No':
        # get the maximum and minimum values of the column
        max_value = gdf[pop_column].max()
        min_value = gdf[pop_column].min()

        # calculate and return the range
        d['pop_range_value'] = max_value - min_value

    # return d

# if state legislative maps,
# population must be exactly equal, allowance to be off by 1 or 2 people


# def pop_difference_legislative(gdf):

#     equality = equal_population(gdf)
    
#     d={}

    # if equality['equal_pop'] == 'No':
        tot_pop = gdf[pop_column].sum()
        # calculate ideal population
        ideal_pop = tot_pop/len(gdf)

        abs_deviation = []
        pct_deviation = []

        for index, row in gdf.iterrows():
            # calculate absolute deviation from ideal population
            abs_dev = row[pop_column] - ideal_pop
            abs_deviation.append(abs_dev)
            
            #calculate % deviation
            pct_dev = abs_dev/row[pop_column]
            pct_deviation.append(pct_dev)
        
        # calculate mean deviation
        mean_deviation = sum(abs_deviation)/len(gdf)

        # calculate the range of deviations
        range_deviation = abs(max(pct_deviation))+abs(min(pct_deviation))

        # dictionary entries
        d['pop_mean_deviation'] = mean_deviation
        d['pop_range_deviation'] = range_deviation

    return d





# def pop_equality(gdf):
#     a= equal_population(gdf)
#     b= pop_difference_congressional(gdf)
#     c= pop_difference_legislative(gdf)
#     return a,b,c
    
    
# test = pop_equality(shp)
