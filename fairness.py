# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 15:07:28 2023

@author: joshu
"""
import pandas as pd
import numpy as np
import geopandas as gpd
from election_2020 import election_2020
from historic_election_data import historic_df_builder
import partisan_fairness as pf
import os
import glob
import warnings
# warnings.filterwarnings("ignore")
# wd = os.getcwd()

# path = wd
# plans = glob.glob(os.path.join(path + "/data/plans/*.csv"))
# # plan = pd.read_csv("./data/pa_no_splits.csv")

def build_geoid(plan, historic, st_fips):
        """
Build a DataFrame by merging redistricting plan and historic election data on constructed geoid20 column.

Parameters:
    plan (str): string of redistricing plan passed to function.
    historic (list): List passed from interface_handler including historic data file in csv format.
    st_fips (str): State FIPS code.

Returns:
    DataFrame: Merged DataFrame containing plan and historic data.
    """
    plan_df = pd.read_csv(plan)
    plan = plan_df.rename(columns={'id': 'geoid20'})
    df = historic_df_builder(plan, historic, st_fips)
    df = df.merge(plan, on='geoid20')
    
    return df

def group_by_party_outcome(df):
        """
Group the DataFrame by district and calculate party outcomes.

Parameters:
    df (DataFrame): DataFrame containing election data.

Returns:
    DataFrame: Grouped DataFrame with summed dem_votes and gop_votes, and calculated d_voteshare.
    """
    
    df_grouped = df.groupby(by='district')['dem_votes', 'gop_votes'].sum()
    df_grouped['d_voteshare'] = df_grouped['dem_votes']/(df_grouped['dem_votes'] + df_grouped['gop_votes'])
    df_grouped.insert(1, 'state', 'PA')
    # df_grouped.insert(1, 'Year', '2018')
    # df_grouped.insert(1, 'Incumbent', 'R')
    # df_grouped.insert(1, 'Party', 'R')
    df_grouped = df_grouped.reset_index().rename(columns = {'index':'district'})
    
    return df_grouped
    
def calc_measures(df_calc):
        """
Calculate voteshare and wasted vote measures from provided DataFrame.

Parameters:
    df_calc (DataFrame): DataFrame containing election data.

Returns:
    dict: Dictionary of plan scores for Efficiency Gap:'eg', Mean-Median Difference: mmd', and Lopsided Margins Test: 'lmt'.
    """
        
    d={}       
    
    #df_calc = df_grouped[['State', 'District' , 'dem_votes', 'gop_votes', 'd_voteshare']]
    # df_calc = df_calc.rename(columns={'dem_votes': 'Dem Votes', 'gop_votes': 'GOP Votes', 'd_voteshare' : 'D Voteshare'})
    df_calc['party'] = np.where(df_calc['dem_votes'] > df_calc['gop_votes'], 'D', 'R')
    df_calc['total'] = df_calc.dem_votes + df_calc.gop_votes
    df_calc['dem_wasted'] = np.where(df_calc['party'] == 'R', df_calc.dem_votes, df_calc.dem_votes - (df_calc.total/2) - .5)
    df_calc['gop_wasted'] = np.where(df_calc['party'] == 'D', df_calc.gop_votes, df_calc.gop_votes - (df_calc.total/2) - .5)
    df_calc['r_voteshare'] = 1 - df_calc['d_voteshare']

    if "Efficiency Gap" in user_input:
        d['eg'] = pf.eg(df_calc)
    if "Mean-Median Difference" in user_input:
        d['mmd'] = pf.mean_median(df_calc)
    if "Lopsided-Margins Test" in user_input:
        d['lmt'] = pf.lmt(df_calc)

    return d

def fairness(plan, historic, st_fips, user_input):
        """
Main function of script. Calculates fairness measures: Efficiency Gap, Mean-Median Difference, Lopsided-Margins Test
    and returns scores for plan as dictionary. Dictionary keys: eg, mmd, lmt
    
Parameters:
    plan (str): string of redistricting plan in .csv format passed to function from list data.
    historic (list): List item of file path to historic election data.
    st_fips (str): State FIPS code passed from geodataframe generated in merge_txt_shp.

Returns:
    dict: Dictionary of calculated fairness measures.
    """

    a= build_geoid(plan, historic, st_fips)
    b= group_by_party_outcome(a)
    c= calc_measures(b, user_input)
    
    return c
