# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 20:03:52 2023

@author: claire
"""

import os
import sys
import geopandas as gpd
import pandas as pd
import statistics as s
import compactness_measures as cm #only use base name of file

#########OUTPUT
## minimum or average or both compactness scores
## minimum because targetting in specific districts

#ask user to specify as parameter which measure they want

#%%
def compact(measures, geo_df):
    
    """Calculates compactness measures based on which measures the user chooses.

    Minimum and mean values are returned for each chosen measure. This gives a
    user an idea of how well a model performs without providing a score for
    each polygon. Some users might pass a thousand plans.

    Parameters
    --------------------------

    measures : list
        Compactness measures chosen by user in the GUI interface.
    geo_df : GeoDataFrame
        Either the geometry file provided by user or the one pulled from the Census API.
        gdf gets passed after polygons have been aggregated by district assignment.

    Returns
    --------------------------
    dictionary
        Dictionary containing names and values of calculated compactness measures.

    Examples
    ------------------------------
   
    >>> compact(['Polsby Popper', 'Convex Hull Ratio'], gdf_vtds)
    {
     "min_pp": 0.03,
     "mean_pp": 0.3,
     "min_hull": 0.2,
     "mean_hull": 0.4
     }

    Example of dictionary returned for one plan passed through compactness()""" 
    
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

