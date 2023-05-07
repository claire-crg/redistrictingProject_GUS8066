# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 15:15:28 2023

@author: claire
"""

import geopandas as gpd

# when function is called in the main function,
# identify which column is the population column
# ask user to specify which column it is?


#get population column
#gdf can either be usre inputted gdf or gdf from census
def get_pop_col(user_input_pop_col, gdf):
    """ Gets column name for population data from GeoDataFrame.
    
    Parameters
    --------------------------
    
    user_input_pop_col: list
        Column names of population data inputted by user in GUI interface.
    gdf : GeoDataFrame
        Geography file after polygons are aggregated.
        Either provided by user or pulled from Census API.
    
    Returns
    --------------------------
    String
        String of population column name.
        
    
    Examples
    ------------------------------
      
    Using GDF provided by user and user specified column in GUI interface:
    >>> get_pop_col(["population"], gdf_aggregated)
    
    "population"
    
    Using GDF from Census API. No column name provided by user in GUI interface:
    >>> get_pop_col([], gdf_aggregated)
    
    "tot_pop"
    
    """
    
    pop_col=None
    ##if from census api pull, I defined the column myself :)
    if 'tot_pop' in gdf.columns:
        pop_col = 'tot_pop'
    # user_input_pop_col will be a list with 1 value
    elif len(user_input_pop_col)> 0 and user_input_pop_col[0] in gdf.columns:
        pop_col = user_input_pop_col[0]
    else:
        print("Can't find the population column")
    
    return pop_col


# see if population is equal in each polygon

def equal_population(gdf, pop_column):
    """ Calculates if there is equal number of population in each polygon.
    
    Parameters
    --------------------------
    
    gdf : GeoDataFrame
        Geography file after polygons are aggregated.
        Either provided by user or pulled from Census API.
    pop_column: String
        Column name of population column in GeoDataFrame
    
    Returns
    --------------------------
    Dictionary
        Says whether there is equal population or not.
        
    
    Examples
    ------------------------------
      
    Using GDF provided by user and user specified column in GUI interface:
    >>> equal_population(gdf_aggregated, ["pop_column"])
    
    {
     "equal_pop" : 'No'
     }
    
    Using GDF from Census API. No column name provided by user in GUI interface:
    >>> equal_population(gdf_aggregated, [])
    
    {
     "equal_pop" : 'No'
     }
    
    """
    
    # empty dictionary to save results
    d = {}
    
    #make sure it is passed as a string
    pop_column = str(get_pop_col(pop_column, gdf))

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
    """ Calculates by how much population quantity varies between polygons.
    
    Parameters
    --------------------------
    
    gdf : GeoDataFrame
        Geography file after polygons are aggregated.
        Either provided by user or pulled from Census API.
    pop_column: String
        Column name of population column in GeoDataFrame
    
    Returns
    --------------------------
    Dictionary
        Measures indicating how much population count differs.
        
    Notes
    -----------------------------
    Measures of population equality:
        1. Range = highest population count - lowest population count
        2. mean_deviation = sum(actual - ideal)/number of polygons
        3. range_deviation = abs(max((actual - ideal)/actual))+abs(min(actual - ideal)/actual))
    
    Examples
    ------------------------------
      
    Using GDF provided by user and user specified column in GUI interface:
    >>> pop_difference(gdf_aggregated, ["pop_column"])
    
    {
     "pop_range_value" : 4048,
     "pop_mean_deviation" : 4.1,
     "pop_range_deviation" : 0.005
     
     }
    
    Using GDF from Census API. No column name provided by user in GUI interface:
    >>> pop_difference(gdf_aggregated, [])
    
    {
     "pop_range_value" : 4048,
     "pop_mean_deviation" : 4.1,
     "pop_range_deviation" : 0.005
     }
    
    """
    
    pop_col= None
    #get pop column name
    if len(pop_column) > 0:
        #get population column from user input
        pop_col = pop_column[0]
    else:
        pop_col = str(get_pop_col(pop_column, gdf))
    
    #make sure population is integer
    gdf[pop_col] = gdf[pop_col].apply(lambda x: int(x))
    
    #see if population is equal
    equality = equal_population(gdf, pop_col)
    
    d={}

    if equality['equal_pop'] == 'No':
        # get the maximum and minimum values of the column
        max_value = gdf[pop_col].max()
        min_value = gdf[pop_col].min()

        # calculate and return the range
        d['pop_range_value'] = max_value - min_value

    # if equality['equal_pop'] == 'No':
        tot_pop = gdf[pop_col].sum()
        # calculate ideal population
        ideal_pop = tot_pop/len(gdf)

        abs_deviation = []
        pct_deviation = []

        for index, row in gdf.iterrows():
            # calculate absolute deviation from ideal population
            abs_dev = row[pop_col] - ideal_pop
            abs_deviation.append(abs_dev)
            
            #calculate % deviation
            pct_dev = abs_dev/row[pop_col]
            pct_deviation.append(pct_dev)
        
        # calculate mean deviation
        mean_deviation = sum(abs_deviation)/len(gdf)

        # calculate the range of deviations
        range_deviation = abs(max(pct_deviation))+abs(min(pct_deviation))

        # dictionary entries
        d['pop_mean_deviation'] = mean_deviation
        d['pop_range_deviation'] = range_deviation

    return d


